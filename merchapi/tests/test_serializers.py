from django.test import TestCase

from merchapi.models import Item, User
from merchapi.serializers.base import ItemSerializer
from merchapi.serializers.item import ItemFavoriteSerializer, ItemPriceSerializer, ItemPriceFavoriteSerializer


class ComposedSerializerTest(TestCase):
    """
    Various tests for the composed serializer decorator.
    """

    def test_composition(self):
        pass
        # todo implement


class ItemSerializerTest(TestCase):
    """
    Various tests for the item serializers.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="test"
        )

    fixtures = ['items.json']

    def test_item_serializer(self):
        item = Item.objects.get(item_id=2)
        self.assertSetEqual(
            set(ItemSerializer(item).data.keys()),
            {'item_id', 'name', 'description', 'store_price', 'members', 'buy_limit', 'high_alch'}
        )

    def test_item_favorite_serializer(self):
        item = Item.objects.with_favorited(self.user.merchant).get(item_id=2)
        self.assertSetEqual(
            set(ItemFavoriteSerializer(item).data.keys()),
            {'item_id', 'name', 'description', 'store_price', 'members', 'buy_limit', 'high_alch', 'favorited'}
        )

    def test_item_price_serializer(self):
        item = list(Item.objects.filter(item_id=2).with_prices())[0]
        self.assertSetEqual(
            set(ItemPriceSerializer(item).data.keys()),
            {'item_id', 'name', 'description', 'store_price', 'members', 'buy_limit', 'high_alch', 'price'}
        )

    def test_item_price_favorite_serializer(self):
        item = list(Item.objects.with_favorited(self.user.merchant).filter(item_id=2).with_prices())[0]
        self.assertSetEqual(
            set(ItemPriceFavoriteSerializer(item).data.keys()),
            {'item_id', 'name', 'description', 'store_price', 'members', 'buy_limit', 'high_alch', 'price', 'favorited'}
        )
