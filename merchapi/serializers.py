from rest_framework import serializers
from merchapi.models import Item


class ItemSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Item
        fields = ('item_id', 'name', 'high_alch', 'store_price', 'buy_limit')
