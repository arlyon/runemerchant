import os

from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from merchapi import ICONS_DIR
from merchapi.models import Item, Price
from util.merch.scrape import get_new_items, get_prices_for_items, download_icons


@db_periodic_task(crontab(day="*"))
def fetch_new_items():
    """
    Gets new items from the api and downloads the icons.
    """
    new_items, _ = get_new_items(1000)
    Item.objects.bulk_create(new_items)

    files = os.listdir(ICONS_DIR)
    item_ids = Item.objects.all().values_list('item_id', flat=True)

    download_icons((item_id for item_id in item_ids if f"{item_id}.gif" not in files), ICONS_DIR)


@db_periodic_task(crontab(hour="*"))
def fetch_new_prices():
    """
    Fetches new prices for all items in the DB.
    """
    prices = get_prices_for_items(Item.objects.all().values_list('item_id', flat=True))
    Price.objects.bulk_create(prices)
