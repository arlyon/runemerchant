from django.db.models import OuterRef, Subquery, Max
from django.test import TestCase, tag

# Create your tests here.
from util.merch.scrape import get_new_items, get_prices_for_ids
from merchapi.models import Price, Item


class MostRecentPrice(TestCase):
    """
    A test ground for getting the most recent price.
    """

    @classmethod
    def setUpTestData(cls):
        items, _ = get_new_items(10)
        Item.objects.bulk_create(items)

        prices = get_prices_for_ids([item.item_id for item in items])
        Price.objects.bulk_create(prices)

    @tag('comparison')
    def test_latest_prices_by_item(self):
        """
        gets a list of the latest price for each item
        """
        with self.assertNumQueries(1):
            latest_prices = list(Price.objects.filter(
                date=Subquery(
                    Price.objects
                        .filter(item=OuterRef('item'))
                        .values('item')
                        .annotate(last_price=Max('date'))
                        .values('last_price')[:1]
                )
            ))

    @tag('comparison')
    def test_latest_buy_price_by_item(self):
        """
        gets a list of items with their latest buy price attached
        """
        with self.assertNumQueries(1):
            price_subquery = Price.objects.filter(pk=OuterRef('item_id')).order_by('-date')
            items_with_buy = list(Item.objects.annotate(latest_price=Subquery(price_subquery.values('buy_price')[:1])))

    @tag('comparison')
    def test_latest_price_log_by_item(self):
        """
        gets a list of items with their latest PriceLog attached
        twice as expensive as just getting out the subquery.
        since it processes in memory, no lazy evaluation
        """
        with self.assertNumQueries(2):
            latest_prices = Price.objects.filter(
                date=Subquery(
                    Price.objects
                        .filter(item=OuterRef('item'))
                        .values('item')
                        .annotate(last_price=Max('date'))
                        .values('last_price')[:1]
                )
            )
            items_with_pricelog = {item.item_id: item for item in Item.objects.all()}
            for price in latest_prices:
                items_with_pricelog[price.item_id].latest_price = price
