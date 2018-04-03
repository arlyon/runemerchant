from django.core.management import BaseCommand

from merchapi.models import Item, PriceLog
from util.merch.scrape import get_prices_for_ids


class Command(BaseCommand):
    help = 'Polls the api for the latest prices for each item in the DB.'

    def handle(self, *args, **options):
        prices = get_prices_for_ids(Item.objects.all())
        PriceLog.objects.bulk_create(prices)

