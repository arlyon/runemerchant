# Generated by Django 2.0.3 on 2018-03-29 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchapi', '0004_tag'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('name', 'item')},
        ),
    ]