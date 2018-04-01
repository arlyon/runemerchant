from rest_framework import serializers

from merchapi.models import PriceLog
from merchapi.serializers.base import ItemSerializer


class PriceLogItemSerializer(serializers.ModelSerializer):
    """
    Serializes a PriceLog with an embedded item.
    """
    item = ItemSerializer()

    class Meta:
        model = PriceLog
        fields = ('date', 'item', 'buy_price', 'sell_price', 'average_price', 'buy_volume', 'sell_volume')