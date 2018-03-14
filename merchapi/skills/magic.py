from typing import Dict

from merchapi.models.item import Rune, Item


def get_rune_prices(runes: Dict[Rune, int]) -> int:
    """
    Gets prices for a list of runes.
    :param runes:
    :return:
    """
    price = 0
    for rune, count in runes.items():
        price += rune.get_most_recent_price() * count

    return price


class MagicManager:
    ALCH_PER_HOUR = 1200

    def __init__(self):
        self.NATURE_RUNE: Rune = Rune.objects.filter(name="Nature rune").first()
        self.FIRE_RUNE: Rune = Rune.objects.filter(name="Fire rune").first()

    def get_high_alch_profit(self, item: Item) -> int:
        """
        Gets the potential profit from high alchemy.
        :return: The profit in gp.
        """

        runes = {
            self.NATURE_RUNE: 1,
            self.FIRE_RUNE: 5
        }

        return item.high_alch - item.get_most_recent_price() - get_rune_prices(runes)

    def get_low_alch_profit(self, item: Item) -> int:
        """
        Gets the potential profit from low alchemy.
        :return: The profit in gp.
        """

        runes = {
            self.NATURE_RUNE: 1,
            self.FIRE_RUNE: 3
        }

        return item.low_alch - item.get_most_recent_price() - get_rune_prices(runes)
