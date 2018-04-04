from rest_framework import serializers

from merchapi.models import Price
from merchapi.serializers.base import ItemSerializer


class PriceItemSerializer(serializers.ModelSerializer):
    """
    Serializes a PriceLog with an embedded item.
    """
    item = ItemSerializer()

    class Meta:
        model = Price
        fields = ('date', 'item', 'buy_price', 'sell_price', 'average_price', 'buy_volume', 'sell_volume')