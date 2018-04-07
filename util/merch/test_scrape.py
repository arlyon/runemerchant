import os
import shutil
from typing import List

from django.test import TestCase

from util.merch.scrape import get_new_items, parse_wiki_data, get_summary, download_icons, get_prices_for_items
from merchapi.models import Item, Price


class ScrapeTest(TestCase):

    def test_get_new_items(self):
        """
        My Test
        :return:
        """
        items, ignored = get_new_items(10)
        Item.objects.bulk_create(items)

        self.assertEqual(Item.objects.all()[0].item_id, 2)

    def test_parse_wiki_data(self):
        result = """return {
            itemId     = 2,
            price      = 172,
            last       = 168,
            date       = '16:34, March 7, 2018 (UTC)',
            lastDate   = '14:51, March 6, 2018 (UTC)',
            volume     = 278.9,
            volumeDate = '16:34, March 7, 2018 (UTC)',
            icon       = 'Cannonball.png',
            item       = 'Cannonball',
            value      = nil,
            limit      = 7000,
            members    = true,
            category   = nil,
            examine    = 'Ammo for the Dwarf Cannon.'
        }"""

        entry = parse_wiki_data(result)

        self.assertEqual(entry["category"], None)
        self.assertEqual(entry["members"], True)
        self.assertEqual(entry["limit"], 7000)
        self.assertEqual(entry["volume"], 278.9)
        self.assertEqual(entry["item"], "Cannonball")

    def test_get_summary(self):
        """
        Checks the osbuddy summary to make sure it works.
        :return:
        """
        self.assertNotEqual(len(get_summary()), 0)

    def test_download_image(self):
        test_path = "./test"
        item_ids = [2]

        download_icons(item_ids, test_path)
        self.assertEqual([f"{item_id}.gif" for item_id in item_ids], os.listdir(test_path))
        shutil.rmtree(test_path)

    def test_get_prices_for_ids(self):
        """
        Tests getting price data for a list of ids.
        :return:
        """
        test_ids = [2, 6]

        test_items, _ = get_new_items(2)
        Item.objects.bulk_create(test_items)

        test_prices: List[Price] = get_prices_for_items(test_ids)

        self.assertEqual([price.item for price in test_prices], test_items)
