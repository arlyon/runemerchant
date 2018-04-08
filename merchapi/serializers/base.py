import itertools

from rest_framework import serializers

from merchapi.models import Item, Tag
from merchapi.models.price import Price


def composed_serializer(serializer):
    """
    A decorator which, when applied to a serializer composed of
    multiple other serializers, generates a Meta that merges the fields.
    :param serializer: The composed class to generate Meta for.
    :return: A new class with correctly defined Meta.
    """

    combined_fields = {x for x in itertools.chain(*(x.Meta.fields for x in serializer.__bases__))}
    if serializer.Meta:
        combined_fields |= set(serializer.Meta.fields)

    class ComposedSerializer(serializer):
        class Meta:
            fields = tuple(combined_fields)
            model = serializer.__base__.Meta.model

    ComposedSerializer.__name__ = serializer.__name__
    ComposedSerializer.__doc__ = serializer.__doc__

    return ComposedSerializer


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializes an item with basic information.
    """

    class Meta:
        model = Item
        fields = ('item_id', 'name', 'description', 'store_price', 'members', 'buy_limit', 'high_alch')


class PriceSerializer(serializers.ModelSerializer):
    """
    Serializes a price log with basic information.
    """

    class Meta:
        model = Price
        fields = ('date', 'item', 'buy_price', 'sell_price', 'average_price', 'buy_volume', 'sell_volume')


class TagSerializer(serializers.ModelSerializer):
    """

    """

    def to_representation(self, tag: Tag):
        return tag.name

    class Meta:
        model = Tag
        fields = ('name',)  # overridden by to_representation
