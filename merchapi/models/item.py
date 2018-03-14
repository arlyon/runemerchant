from django.db import models

from merchapi.models.flip import PriceLog, Flip
from merchapi.models.user import Merchant


class MissingItem(models.Model):
    """
    An item to be ignored by the aggregator.
    """
    item_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)


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

    def get_most_recent_price(self) -> PriceLog or None:
        """
        Gets and saves price data for a particular item from the API.
        todo price data service that either gets cache or fetches
        :return: The price log data for the given item.
        """
        return PriceLog.objects.filter(item=self).order_by('-date').first()

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
        return "[" + str(self.item_id) + "] " + self.name

    class Meta:
        verbose_name_plural = "Items"


class Rune(Item):
    """
    A rune in runescape.
    """
    def get_usages(self):
        pass
