# Generated by Django 3.2.7 on 2021-11-03 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rarity', '0018_asset_decoded_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='description',
        ),
    ]
