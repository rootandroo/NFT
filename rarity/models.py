from os import memfd_create
from django.db import models
from django.db.models.base import ModelState
from django.db.models.fields import SlugField


class Project(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    twitter = models.URLField(max_length=23, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Collection(models.Model):
    policy_id = models.CharField(max_length=56, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collections')
    included_keys = models.JSONField(null=True)
    distribution = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['project']

    def __str__(self):
        return f"{self.project}"

    def save(self, *args, **kwargs):
        if self.included_keys:
            # Update distribution
            keys = self.included_keys
            assets = self.assets.all()
            self.distribution = self.fetch_distribution(keys, assets)

            # Set Asset Score
            for asset in assets:
                asset.set_score(self.distribution, keys, len(assets))
        super().save(*args, **kwargs)


    def fetch_distribution(self, keys, assets):
        def parse_obj(key, object):
            if type(object) is list:
                for elem in object:
                    parse_obj(key, elem)
            elif object:
                if key in dist:
                    dist[key][object] = dist[key].get(object, 0) + 1
                else:
                    dist[key] = {}
                    dist[key][object] = 1
            else:
                if key in dist:
                    dist[key]['null'] = dist[key].get('null', 0) + 1
                else:
                    dist[key] = {}
                    dist[key]['null'] = 1
        dist = {}
        for key in keys:
            for asset in assets:
                metadata = asset.onchain_metadata
                if key in metadata:
                    parse_obj(key, metadata[key])                    
                else:
                    parse_obj(key, '')
        return dist            


class Asset(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    policy_id = models.CharField(max_length=56)
    fingerprint = models.CharField(max_length=44, unique=True)
    quantity = models.PositiveBigIntegerField()
    mint_tx_hash = models.CharField(max_length=64)
    onchain_metadata = models.JSONField(null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='assets')
    score = models.DecimalField(max_digits=8, decimal_places=2, null=True)    

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return self.ascii_name

    def set_score(self, distribution, included_keys, total_count):
        total = 0
        for key in included_keys:
            metadata = self.onchain_metadata
            if key in metadata:
                value = 'null' if metadata[key] == '' else metadata[key]
                count = distribution[key][value]
                trait_score = 1 / (count / total_count)
                total += trait_score
        self.score = total
        self.save()

    @property
    def ascii_name(self):
        bytes_obj = bytes.fromhex(self.name)
        return bytes_obj.decode('ASCII')
    
