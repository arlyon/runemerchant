from django.core.management import BaseCommand

from merchapi.models import Item
from util.merch.scrape import get_new_items


class Command(BaseCommand):
    help = 'Polls the api for the latest items.'

    def handle(self, *args, **options):

        new_items, missing_items = get_new_items(1000)
        Item.objects.bulk_create(new_items)

