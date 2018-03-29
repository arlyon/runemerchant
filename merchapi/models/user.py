from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Merchant(models.Model):
    """
    A merchant.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField('Item', through='Favorite')


class Favorite(models.Model):
    """
    A favorite for a user.
    """
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    user = models.ForeignKey(Merchant, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('item', 'user')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Links the merchant and user together.
    """
    if created:
        Merchant.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the merchant when the user changes.
    """
    instance.merchant.save()