from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from merchapi.models import Price
from merchapi.serializers.base import PriceSerializer, composed_serializer, ItemSerializer


@composed_serializer
class ItemFavoriteSerializer(ItemSerializer):
    """
    Serializes an item embedding whether it has been
    favorited. Requires Item.with_favorite()
    """
    favorited = serializers.BooleanField()

    class Meta:
        fields = ('favorited',)


@composed_serializer
class ItemPriceSerializer(ItemSerializer):
    """
    Serializes an Item and embeds the most recent
    price log. Better performance for many items.
    Requires Items.with_prices()
    """
    price = PriceSerializer()

    class Meta:
        fields = ('price',)


@composed_serializer
class ItemPriceFavoriteSerializer(ItemFavoriteSerializer, ItemPriceSerializer):
    """
    A composed serializer consisting of favorites.
    """
    pass


@composed_serializer
class SingleItemPriceSerializer(ItemSerializer):
    """
    Serializes an Item and embeds the most recent
    price log. Better performance for a single item.
    """
    price = SerializerMethodField()

    @staticmethod
    def get_price(item):
        """
        Gets the latest price, or none if it does not exist.
        :param item: The item to look up.
        :return: The latest price log for that item.
        """
        try:
            return PriceSerializer(item.price_set.latest('-date')).data
        except Price.DoesNotExist:
            return None

    class Meta:
        fields = ('price',)


@composed_serializer
class SingleItemPriceFavoriteSerializer(ItemFavoriteSerializer, SingleItemPriceSerializer):
    """
    A composed serializer consisting of favorites.
    """
    pass
