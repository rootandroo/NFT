# Generated by Django 3.2.7 on 2021-11-01 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rarity', '0014_asset_decoded_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='decoded_name',
        ),
    ]
