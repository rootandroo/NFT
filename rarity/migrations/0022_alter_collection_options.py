# Generated by Django 3.2.7 on 2021-11-14 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rarity', '0021_alter_collection_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['release_date']},
        ),
    ]
