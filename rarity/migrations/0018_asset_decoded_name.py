# Generated by Django 3.2.7 on 2021-11-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rarity', '0017_auto_20211103_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='decoded_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
