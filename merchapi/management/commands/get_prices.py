from django.core.management import BaseCommand

from merchapi.models import Item, Price
from util.merch.scrape import get_prices_for_items


class Command(BaseCommand):
    help = 'Polls the api for the latest prices for each item in the DB.'

    def handle(self, *args, **options):
        prices = get_prices_for_items(Item.objects.all().values_list('item_id', flat=True))
        Price.objects.bulk_create(prices)
