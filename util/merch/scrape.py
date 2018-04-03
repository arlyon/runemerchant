import errno
import os
import shutil
from datetime import datetime
from typing import List, Tuple, Dict

import requests

from merchapi.models import MissingItem, Item, PriceLog

ITEM_SUMMARY_URL = "https://rsbuddy.com/exchange/summary.json"
RUNESCAPE_WIKI_URL = "http://2007.runescape.wikia.com/wiki/Module:Exchange/%s?action=raw"
RUNESCAPE_IMAGE_URL = "https://services.runescape.com/m=itemdb_oldschool/obj_big.gif?id="
OSBUDDY_API = "https://api.rsbuddy.com/grandExchange?a=guidePrice"


def get_summary() -> List[Dict]:
    """
    Queries the summary url for the latest list of items.
    :return:
    """
    return requests.get(ITEM_SUMMARY_URL).json().values()


def get_wiki_item(name: str) -> Dict or None:
    """
    Gets wiki data for a given item.
    :param name: The name of the item to look up.
    :return: A dictionary with the data.
    """
    wiki_info = requests.get(url=RUNESCAPE_WIKI_URL % name)
    return parse_wiki_data(wiki_info.text) if wiki_info.status_code != 404 else None


def parse_wiki_data(wiki_response: str) -> Dict[str, str or int or float or bool or None]:
    """
    Parses the data string from the wiki API
    :param wiki_response: The text response from the wiki.
    :return: A dictionary with the data.
    """
    data = {pair[0].strip(): pair[-1].strip() for pair in
            (line.split("=", 1) for line in wiki_response.splitlines()[1:-1])}

    for key, value in data.items():
        if value[-1] == ",":
            value = value[0:-1]

        if value == 'nil':
            value = None
        elif value[0] == "'" and value[-1] == "'":
            value = value[1:-1]
        elif value == 'true' or value == 'false':
            value = value == 'true'
        elif value.isdigit():
            value = int(value)
        elif value.replace('.', '', 1).isdigit():
            value = float(value)

        data[key] = value

    return data


def download_icons(item_ids: List[int], folder: str) -> None:
    """
    Downloads the icons for the given list of item ids.
    :param item_ids: The list of item ids to download.
    :param folder: The folder to download them to.
    :return: None.
    """
    try:
        os.makedirs(folder)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    images = os.listdir(folder)
    total = len(item_ids)
    count = 1

    for item_id in (x for x in item_ids if f"{x}.gif" not in images):
        response = requests.get(RUNESCAPE_IMAGE_URL + str(item_id), stream=True)
        with open(os.path.join(folder, f"{item_id}.gif"), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        print(f"Downloaded {count} out of {total} ({item_id}.gif)")
        count += 1


def get_new_items(quantity: int or None = None) -> Tuple[List[Item], List[MissingItem]]:
    """
    Searches and returns a list of any new items not yet in the database.
    :return: A list of the new items.
    """

    items = set()

    counter = 0
    item_ids = Item.objects.all().values_list('item_id', flat=True)

    new_items = []
    ignored_items = []

    for data in get_summary():
        if data["id"] in item_ids:
            continue

        counter += 1

        if quantity is not None and counter > quantity:
            break

        wiki_info = get_wiki_item(data["name"])

        if wiki_info is not None and wiki_info["examine"] is not None and wiki_info["members"] is not None:
            items |= wiki_info.keys()
            new_item = Item(item_id=data["id"],
                            name=data["name"],
                            members=wiki_info["members"],
                            description=wiki_info["examine"],
                            high_alch=wiki_info["hialch"] if "hialch" in wiki_info else None,
                            low_alch=wiki_info["lowalch"] if "lowalch" in wiki_info else None,
                            buy_limit=wiki_info["limit"],
                            store_price=data["sp"] if "sp" in data else None)
            new_items.append(new_item)
        else:
            ignored_item = MissingItem(item_id=data["id"], name=data["name"])
            ignored_items.append(ignored_item)

    return new_items, ignored_items


def get_prices_for_ids(item_ids: List[int]) -> List[PriceLog]:
    """
    Queries the OSBuddy api for the guide prices of a given list of item ids.
    :param item_ids: The list of items.
    :return: A list of PriceLogs with the date,
    """
    price_data: List[PriceLog] = []

    if len(item_ids) > 100:
        chunks = (item_ids[i:i + 100] for i in range(0, len(item_ids), 100))

        for chunk in chunks:
            price_data += get_prices_for_ids(chunk)
    else:
        url = OSBUDDY_API + "".join(f"&i={item_id}" for item_id in item_ids)

        request = requests.get(url)
        if request.status_code == 200:
            raw_data = request.json()
        else:
            raise Exception(f"Error with API: {request.status_code}")

        for item_id, data in raw_data.items():
            price_data.append(PriceLog(
                date=datetime.now(),
                buy_price=data["buying"],
                sell_price=data["selling"],
                average_price=data["overall"],
                buy_volume=data["buyingQuantity"],
                sell_volume=data["sellingQuantity"],
                item=Item.objects.filter(item_id=item_id).first()
            ))

    return price_data
