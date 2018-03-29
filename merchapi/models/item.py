from django.db import models

from merchapi.models.flip import PriceLog, Flip
from merchapi.models.user import Merchant


class MissingItem(models.Model):
    """
    An item to be ignored by the aggregator.
    """
    item_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)


class ItemManager(models.QuerySet):

    def with_recent_price(self):
        """
        Adds the most recent flip to the returned items.
        :return:
        """
        pass


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

    def get_most_recent_price(self) -> PriceLog or None:
        """
        Gets and saves price data for a particular item from the API.
        todo price data service that either gets cache or fetches
        :return: The price log data for the given item.
        """
        return PriceLog.objects.filter(item=self).latest('date')

    def get_profit(self, merchant: Merchant) -> int:
        """
        Returns the total profit earned on this item for a specific user.
        :param merchant: The user to check.
        :return: The amount of profit made.
        """
        profit = 0

        for flip in Flip.objects.filter(item=self, merchant=merchant):
            profit += flip.get_profit_total()

        return profit

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Items"


class Tag(models.Model):
    name = models.CharField(max_length=256)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'item')


class Rune(Item):
    """
    A rune in runescape.
    """

    def get_usages(self):
        pass
