# Generated by Django 3.2.7 on 2021-10-26 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rarity', '0013_asset_market'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='decoded_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
