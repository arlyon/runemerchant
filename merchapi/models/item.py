from typing import Iterable, Dict

from django.db import models
from django.db.models import Count, Q, F, Sum, QuerySet, Subquery, OuterRef, Max
from django.db.models.functions import Cast

from merchapi.models.flip import Flip
from merchapi.models.price import Price
from merchapi.models.user import Merchant


class MissingItem(models.Model):
    """
    An item to be ignored by the aggregator.
    """
    item_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)


class ItemManager(models.QuerySet):

    def with_favorited(self, merchant: Merchant) -> QuerySet:
        """
        Annotates the items with the favorited status for a user.
        :param merchant: The merchant to get the favorites for.
        :return: A queryset with favorites annotated.
        """
        return self.annotate(favorited=Cast(Count('favorite', filter=Q(favorite__merchant=merchant)), models.BooleanField()))

    def with_prices(self) -> Iterable['Item']:
        """
        Takes a queryset of Items and merges in price data.
        :return: An iterable.
        """

        def item_generator(items: Iterable[Item], price_logs: Dict[int, Price]):
            for item in items:
                item.price = price_logs[item.item_id] if item.item_id in price_logs else None
                yield item

        latest_prices = Price.objects.filter(
            date=Subquery(
                Price.objects
                    .filter(item=OuterRef('item'))
                    .values('item')
                    .annotate(last_price=Max('date'))
                    .values('last_price')[:1]
            )
        )

        return item_generator(
            self.order_by('item_id'),
            {price_log.item_id: price_log for price_log in latest_prices}
        )


class Item(models.Model):
    """
    An item in Runescape.
    """
    item_id = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=256, db_index=True)
    description = models.CharField(max_length=256)
    members = models.BooleanField()

    store_price = models.IntegerField(blank=True, null=True)
    buy_limit = models.IntegerField(blank=True, null=True)
    high_alch = models.IntegerField(blank=True, null=True)
    low_alch = models.IntegerField(blank=True, null=True)

    favorites = models.ManyToManyField(Merchant, through='Favorite')

    objects = ItemManager.as_manager()

    def get_most_recent_price(self) -> Price or None:
        """
        Gets and saves price data for a particular item from the API.
        :return: The price log data for the given item.
        """
        return Price.objects.filter(item=self).latest('date')

    def get_profit(self, merchant: Merchant) -> int:
        """
        Returns the total profit earned on this item for a specific user.
        :param merchant: The user to check.
        :return: The amount of profit made.
        """
        return Flip.objects.filter(item=self, merchant=merchant)\
            .annotate(profit=(F('sell_price') - F('buy_price')) * F('quantity'))\
            .aggregate(Sum('profit'))["profit__sum"] or 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Items"


class TaggedItem(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(Merchant, on_delete=models.CASCADE, default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tagged Items"
        unique_together = (('tag', 'item', 'user'),)


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)
    items = models.ManyToManyField('Item', through=TaggedItem, related_name='tags')

    class Meta:
        verbose_name_plural = "Tags"


class Rune(Item):
    """
    A rune in runescape.
    """
    pass
