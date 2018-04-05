from django.db import models
from django.db.models import Count, Q, F, Sum

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

    def with_favorited(self, user):
        """
        Annotates the items with the favorited status for a user.
        :param user: The user to get the favorites for.
        :return:
        """
        return self.annotate(favorited=Count('favorite', filter=Q(favorite__user_id=user.id)))


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

    def get_usages(self):
        pass
