import os

from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from merchapi.models import Item, Price, BASE_DIR
from util.merch.scrape import get_new_items, get_prices_for_items, download_icons


@db_periodic_task(crontab(day="*"))
def fetch_new_items():
    """
    Gets new items from the api and downloads the icons.
    :return:
    """
    new_items, missing_items = get_new_items(1000)
    Item.objects.bulk_create(new_items)

    icons_dir = os.path.join(BASE_DIR, 'merchapi/static/icons')

    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)

    files = os.listdir(icons_dir)
    item_ids = Item.objects.all().values_list('item_id', flat=True)

    download_icons((x for x in item_ids if f"{x}.gif" not in files), icons_dir)


@db_periodic_task(crontab(hour="*"))
def fetch_new_prices():
    prices = get_prices_for_items(Item.objects.all().values_list('item_id', flat=True))
    Price.objects.bulk_create(prices)
