import datetime

from django.test import TestCase

from merchapi.models import Item, Price, User, Flip, Spell


class ItemTest(TestCase):
    fixtures = ['items.json']

    def setUp(self):
        self.item = Item.objects.get(item_id=2)

        self.merchant = User.objects.create(
            username="test",
            password="secret",
            email="test@test.com",
        ).merchant

        self.merchant2 = User.objects.create(
            username="test2",
            password="secret2",
            email="test@test.com2",
        ).merchant

        self.first_price = Price.objects.create(
            date=datetime.datetime.now() - datetime.timedelta(seconds=10),
            item=self.item,
            user=None,
            buy_price=5,
            sell_price=3,
            average_price=4,
            buy_volume=200,
            sell_volume=300,
        )

        self.second_price = Price.objects.create(
            date=datetime.datetime.now(),
            item=self.item,
            user=None,
            buy_price=5,
            sell_price=3,
            average_price=4,
            buy_volume=200,
            sell_volume=300,
        )

        Flip.objects.create(
            item=self.item,
            merchant=self.merchant,
            quantity=100,

            buy_price=2,
            sell_price=3,

            order_date=datetime.datetime.now() - datetime.timedelta(minutes=10),
            buy_date=datetime.datetime.now() - datetime.timedelta(minutes=8),
            listed_date=datetime.datetime.now() - datetime.timedelta(minutes=6),
            sell_date=datetime.datetime.now() - datetime.timedelta(minutes=4),
        )

    def test_most_recent_price(self):
        self.assertEqual(self.item.get_most_recent_price(), self.second_price)

    def test_profit(self):
        self.assertEqual(self.item.get_profit(self.merchant), 100)
        self.assertEqual(self.item.get_profit(self.merchant2), 0)


class PriceTest(TestCase):
    fixtures = ['items.json']

    def setUp(self):
        self.item = Item.objects.get(item_id=2)

        self.price = Price.objects.create(
            date=datetime.datetime.now(),
            item=self.item,
            user=None,
            buy_price=3,
            sell_price=6,
            average_price=4,
            buy_volume=200,
            sell_volume=300,
        )

    def test_roi(self):
        self.assertEqual(self.price.get_roi(), 2)

    def test_profit(self):
        self.assertEqual(self.price.get_profit(), 3)

    def test_demand(self):
        self.assertAlmostEqual(self.price.get_demand(), 2 / 3)


class FlipTest(TestCase):
    # todo implement when adding flips

    def test_get_duration(self):
        pass

    def test_get_profit_per_hour(self):
        pass

    def test_get_roi(self):
        pass

    def test_get_profit_each(self):
        pass

    def test_get_profit_total(self):
        pass

    def test_get_flip_state(self):
        pass


class SpellTest(TestCase):
    fixtures = ['items.json', 'spells.json', 'runes.json', 'requiredrunes.json']

    def setUp(self):

        Price.objects.create(
            date=datetime.datetime.now(),
            item=Item.objects.get(name="Air rune"),
            user=None,
            buy_price=3,
            sell_price=6,
            average_price=4,
            buy_volume=200,
            sell_volume=300,
        )

        Price.objects.create(
            date=datetime.datetime.now(),
            item=Item.objects.get(name="Mind rune"),
            user=None,
            buy_price=3,
            sell_price=6,
            average_price=4,
            buy_volume=200,
            sell_volume=300,
        )

    def test_get_price(self):
        spell = Spell.objects.get(name="Wind Strike")
        required_runes = spell.requiredrunes_set.all()
        price = 0
        for required_rune in required_runes:
            price += required_rune.rune.get_most_recent_price().buy_price * required_rune.quantity

        with self.assertNumQueries(2):
            self.assertEqual(spell.get_price(), price)
