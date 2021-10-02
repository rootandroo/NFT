# Generated by Django 3.2.7 on 2021-10-02 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('twitter', models.URLField(blank=True, max_length=23)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('policy_id', models.CharField(max_length=56, primary_key=True, serialize=False)),
                ('included_keys', models.JSONField(null=True)),
                ('distribution', models.JSONField(null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='rarity.project')),
            ],
            options={
                'ordering': ['project'],
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('policy_id', models.CharField(max_length=56)),
                ('fingerprint', models.CharField(max_length=44, unique=True)),
                ('quantity', models.PositiveBigIntegerField()),
                ('mint_tx_hash', models.CharField(max_length=64)),
                ('onchain_metadata', models.JSONField(null=True)),
                ('score', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='rarity.collection')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
