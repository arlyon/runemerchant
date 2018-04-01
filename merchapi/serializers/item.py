from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from merchapi.models import PriceLog
from merchapi.serializers.base import PriceLogSerializer, composed_serializer, ItemSerializer


@composed_serializer
class ItemFavoriteSerializer(ItemSerializer):
    """

    """
    favorited = serializers.BooleanField()

    class Meta:
        fields = ('favorited',)


@composed_serializer
class ItemPriceLogSerializer(ItemSerializer):
    """
    Serializes an Item and embeds the most recent price log.
    """
    price_log = SerializerMethodField()

    @staticmethod
    def get_price_log(item):
        """
        Gets the latest price, or none if it does not exist.
        :param item: The item to look up.
        :return: The latest price log for that item.
        """
        try:
            return PriceLogSerializer(item.pricelog_set.latest('-date')).data
        except PriceLog.DoesNotExist:
            return None

    class Meta:
        fields = ('price_log',)


@composed_serializer
class ItemPriceLogFavoriteSerializer(ItemFavoriteSerializer, ItemPriceLogSerializer):
    """
    A composed serializer consisting of favorites.
    """
    pass

