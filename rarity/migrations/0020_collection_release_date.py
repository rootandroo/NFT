# Generated by Django 3.2.7 on 2021-11-03 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rarity', '0019_remove_collection_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
