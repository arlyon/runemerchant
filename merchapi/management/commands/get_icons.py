import os
from django.core.management import BaseCommand

from merchapi import ICONS_DIR
from merchapi.models import Item
from util.merch.scrape import download_icons


class Command(BaseCommand):
    help = 'Downloads all missing icons.'

    def handle(self, *args, **options):
        if not os.path.exists(ICONS_DIR):
            os.makedirs(ICONS_DIR)

        files = os.listdir(ICONS_DIR)
        item_ids = Item.objects.all().values_list('item_id', flat=True)

        download_icons((x for x in item_ids if f"{x}.gif" not in files), ICONS_DIR)
