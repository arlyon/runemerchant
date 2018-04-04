from enum import Enum

from django.db import models
from django.conf import settings
from datetime import timedelta

from merchapi.models.user import Merchant

BASE_DIR = settings.BASE_DIR
OS_BUDDY = 'https://api.rsbuddy.com/grandExchange?a=guidePrice&i='


class IncompleteFlipError(Exception):
    pass


class FlipState(Enum):
    """
    The states of a flip.
    """
    INVALID = 0
    BUYING = 10
    BANK = 20
    SELLING = 30
    SOLD = 40


class Flip(models.Model):
    """
    The base class for a transaction consisting of a buy order and a sell order.
    """
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    buy_price = models.PositiveIntegerField(default=1)
    sell_price = models.PositiveIntegerField(null=True, blank=True)

    order_date = models.DateTimeField()
    buy_date = models.DateTimeField(null=True, blank=True)
    listed_date = models.DateTimeField(null=True, blank=True)
    sell_date = models.DateTimeField(null=True, blank=True)

    def get_duration(self) -> timedelta:
        """
        Gets the total amount of time the sale took.
        :return: The duration of the flip.
        :raises IncompleteFlipError: When the flip is incomplete.
        """
        if self.get_flip_state() == FlipState.SOLD:
            return self.sell_date - self.order_date
        else:
            raise IncompleteFlipError('Cannot calculate duration on incomplete flip.')

    def get_profit_per_hour(self) -> float or None:
        """
        Gets the total profit per hour of the flip.
        :return: The profit in gp.
        :raises IncompleteFlipError: When the flip is incomplete.
        """
        try:
            return self.get_profit_total() / (self.get_duration().seconds / 3600)
        except IncompleteFlipError:
            raise IncompleteFlipError('Cannot calculate profit on incomplete flip.')

    def get_roi(self) -> float:
        """
        Calculates the return on investment.
        :return: The roi in decimal format.
        :raises IncompleteFlipError: When the flip is incomplete.
        """
        if self.get_flip_state() == FlipState.SELLING:
            return self.sell_price / self.buy_price
        else:
            raise IncompleteFlipError('Cannot calculate roi with no sell price.')

    def get_profit_each(self) -> int:
        """
        Returns the profit per item.
        :return: The profit per item in gp.
        :raises IncompleteFlipError: When the flip is incomplete.
        """
        if self.get_flip_state() == FlipState.SELLING:
            return self.sell_price - self.buy_price
        else:
            raise IncompleteFlipError('Cannot calculate profit with no sell price.')

    def get_profit_total(self) -> int:
        """
        Returns the profit amount overall.
        :return: The total profit in gp.
        :raises IncompleteFlipError: When the flip is incomplete.
        """
        return self.quantity * self.get_profit_each()

    def get_flip_state(self) -> FlipState:
        """
        Returns the status of the flip (buy/bank/sell/sold)
        :return: A FlipState representing the status of the flip.
        """
        if self.sell_date is not None:
            return FlipState.SOLD
        elif self.listed_date is not None and self.sell_price is not None:
            return FlipState.SELLING
        elif self.buy_date is not None:
            return FlipState.BANK
        elif self.order_date is not None and self.buy_price is not None:
            return FlipState.BUYING
        else:
            return FlipState.INVALID

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name_plural = "Flips"
