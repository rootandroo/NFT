# Generated by Django 3.2.7 on 2021-10-06 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rarity', '0005_asset_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]