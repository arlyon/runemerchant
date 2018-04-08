from rest_framework import serializers

from merchapi.models import Price
from merchapi.serializers.base import ItemSerializer, PriceSerializer


class PriceItemSerializer(PriceSerializer):
    """
    Serializes a PriceLog with an embedded item.
    """
    item = ItemSerializer()