from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from merchapi.models import Item, PriceLog


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializes an item with basic information.
    """

    class Meta:
        model = Item
        fields = ('item_id', 'name', 'store_price', 'members', 'buy_limit', 'high_alch')


class PriceLogItemSerializer(serializers.ModelSerializer):
    """
    Serializes a PriceLog with an embedded item.
    """
    item = ItemSerializer()

    class Meta:
        model = PriceLog
        fields = ('date', 'item', 'buy_price', 'sell_price', 'average_price', 'buy_volume', 'sell_volume')


class PriceLogSerializer(serializers.ModelSerializer):
    """
    Serializes a price log with basic information.
    """

    class Meta:
        model = PriceLog
        fields = ('date', 'item', 'buy_price', 'sell_price', 'average_price', 'buy_volume', 'sell_volume')


class ItemPriceLogSerializer(serializers.ModelSerializer):
    """
    Serializes an Item and embeds the most recent price log.
    """
    price_log = SerializerMethodField()

    @staticmethod
    def get_price_log(item):
        return PriceLogSerializer(item.pricelog_set.latest('-date')).data

    class Meta:
        model = Item
        fields = (
            'item_id', 'name', 'description', 'store_price', 'members', 'buy_limit', 'high_alch', 'low_alch',
            'price_log')