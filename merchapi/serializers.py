from rest_framework import serializers
from merchapi.models import Item, PriceLog


class ItemListSerializer(serializers.ModelSerializer):
    """
    The basic class for serializing an item.
    """

    class Meta:
        model = Item
        fields = ('item_id', 'name', 'store_price', 'members', 'buy_limit', 'high_alch')


class ItemSerializer(serializers.ModelSerializer):
    """
    A more detailed view that additionally calculates
    profit, roi and demand for an item.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.price_log: PriceLog = None

    profit = serializers.SerializerMethodField()
    roi = serializers.SerializerMethodField()
    demand = serializers.SerializerMethodField()

    latest_price = serializers.IntegerField()

    class Meta:
        model = Item
        fields = (
            'item_id', 'name', 'description', 'store_price', 'members', 'buy_limit', 'high_alch', 'low_alch', 'profit',
            'roi', 'demand', 'latest_price')

    def get_profit(self, item: Item):
        if self.price_log is None:
            self.price_log = item.get_most_recent_price()
        return None if self.price_log is None else self.price_log.get_profit()

    def get_roi(self, item: Item):
        if self.price_log is None:
            self.price_log = item.get_most_recent_price()
        return None if self.price_log is None else self.price_log.get_roi()

    def get_demand(self, item: Item):
        if self.price_log is None:
            self.price_log = item.get_most_recent_price()
        return None if self.price_log is None else self.price_log.get_demand()


class PriceLogSerializer(serializers.ModelSerializer):
    """

    """
    item = ItemListSerializer()

    class Meta:
        model = PriceLog
        fields = ('date', 'item', 'buy_price', 'sell_price', 'average_price', 'buy_volume', 'sell_volume')
