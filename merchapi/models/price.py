from typing import Iterable

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, FloatField, Subquery, OuterRef, Max
from django.db.models.functions import Cast


class PriceManager(models.QuerySet):
    """
    A price manager.
    """

    def calculate_data(self):
        return self.annotate(
            profit=F('sell_price') - F('buy_price'),
            roi=Cast(F('sell_price'), FloatField()) / Cast(F('buy_price'), FloatField()),
            demand=Cast(F('buy_volume'), FloatField()) / Cast(F('sell_volume'), FloatField())
        )

    def most_recent_for_each_item(self, items: Iterable=None):
        """
        Gets the most recent price for a list of items (or all of them)
        :param items: A list of items to get the price of.
        :return: 
        """
        sub_query = Price.objects.filter(item=OuterRef('item'))\
                        .values('item')\
                        .annotate(last_price=Max('date'))\
                        .values('last_price')[:1]
        
        return self.filter(date=Subquery(sub_query)) \
            if items is None else \
            self.filter(item__in=items).filter(date=Subquery(sub_query))


class Price(models.Model):
    """
    A single piece of price data for an item.
    """
    date = models.DateTimeField()
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    buy_price = models.IntegerField(blank=True, null=True)
    sell_price = models.IntegerField(blank=True, null=True)
    average_price = models.IntegerField(blank=True, null=True)

    buy_volume = models.IntegerField(blank=True, null=True)
    sell_volume = models.IntegerField(blank=True, null=True)

    objects = PriceManager.as_manager()

    def get_profit(self) -> int or None:
        """
        Calculates the profit for the item.
        :return: The profit, or None if buy or sell price is unknown.

        .. note::
            Buying for 4gp and selling for 5gp is a profit of 1gp
        """
        if self.sell_price is not None and self.buy_price is not None:
            return self.sell_price - self.buy_price
        else:
            return None

    def get_roi(self) -> float or None:
        """
        Calculates the roi for the item.
        :return: The return on investment, or None if buy or sell price is unknown.

        .. note::
            Buying for 4gp and selling for 5gp is an roi of 1.25 or 25%
        """
        if self.sell_price is not None and self.buy_price is not None:
            return self.sell_price / self.buy_price
        else:
            return None

    def get_demand(self) -> float or None:
        """
        Calculates the demand for item.
        :return: The demand, or None if buy or sell volume is unknown.

        .. note::
            A buy volume of 2000 and a sell volume of 10 would put the
            demand at 200:1 returning 200.
        """
        if self.buy_volume is not None and self.sell_volume is not None:
            return self.buy_volume / self.sell_volume
        else:
            return None

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name_plural = "Prices"
