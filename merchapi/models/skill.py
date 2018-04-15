from django.db import models

from merchapi.models import Rune, Price


class Spell(models.Model):
    """
    A spell in runescape.
    """
    name = models.CharField(max_length=256)
    level = models.PositiveIntegerField()
    xp = models.FloatField()
    runes = models.ManyToManyField(Rune, through='RequiredRunes')

    def get_price(self) -> int:
        """
        Gets the price of casting the given spell.
        :return: The price in gp.
        """

        required_runes = self.requiredrunes_set.select_related('rune').all()
        prices = {price.item_id: price for price in
                  Price.objects.most_recent_for_each_item(req.rune for req in required_runes)}
        return sum(req.quantity * prices[req.rune.item_id].buy_price for req in required_runes)

    def __str__(self):
        return f"[{self.level}] {self.name}"


class RequiredRunes(models.Model):
    """
    Lists the required runes for a spell.
    """
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    rune = models.ForeignKey(Rune, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.rune.name} - {self.spell.name}"

    class Meta:
        unique_together = ('spell', 'rune')
        verbose_name_plural = "Required Runes"
