# Generated by Django 2.0.3 on 2018-03-29 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchapi', '0002_auto_20180313_0048'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('item', 'user')},
        ),
    ]
