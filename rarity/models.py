from django.db import models
from .services import fetch_all_assets, flatten_metadata, validate_policy_id


class Project(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    query_name = models.CharField(max_length=64, blank=True)
    twitter = models.URLField(max_length=23, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args,  **kwargs):
        self.query_name = self.name.replace(' ', '')
        super().save(*args, **kwargs)


class Collection(models.Model):
    policy_id = models.CharField(max_length=56, primary_key=True, validators=[validate_policy_id])
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collections')
    included_keys = models.JSONField(null=True, blank=True)
    distribution = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['project']

    def __str__(self):
        return f"{self.project}"

    def save(self, *args, **kwargs):
        # Fetch and Create Assets
        if not self.assets.all():
            asset_list = fetch_all_assets(self.policy_id)
            for asset in asset_list:
                asset_obj = Asset(
                    name=asset['asset_name'],
                    policy_id=asset['policy_id'],
                    fingerprint=asset['fingerprint'],
                    quantity=asset['quantity'],
                    mint_tx_hash=asset['initial_mint_tx_hash'], 
                    onchain_metadata=flatten_metadata(asset['onchain_metadata']),
                    collection=self)
                asset_obj.save()

        if self.included_keys:
            # Update distribution
            keys = self.included_keys
            assets = self.assets.all()
            self.distribution = self.fetch_distribution(keys, assets)

            # Set Asset Score and ID
            for asset in assets:
                asset.set_score(self.distribution, keys, len(assets))
                asset.set_id()

            # Set Asset Rank
            for rank, asset_obj in enumerate(assets.order_by('-score')):
                asset_obj.rank = rank + 1
                asset_obj.save()
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
                # Missing either or both of key:value pair
                asset.onchain_metadata[key] = None
                asset.save()

                if key in dist:
                    dist[key][None] = dist[key].get(None, 0) + 1
                else:
                    dist[key] = {}
                    dist[key][None] = 1
        dist = {}
        for key in keys:
            for asset in assets:
                metadata = asset.onchain_metadata
                if key in metadata:
                    parse_obj(key, metadata[key])
                else:
                    parse_obj(key, None)
        return dist            


class Asset(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    policy_id = models.CharField(max_length=56)
    fingerprint = models.CharField(max_length=44, unique=True)
    quantity = models.PositiveBigIntegerField()
    mint_tx_hash = models.CharField(max_length=64)
    onchain_metadata = models.JSONField(null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='assets')
    score = models.DecimalField(max_digits=8, decimal_places=2, null=True)    
    rank = models.PositiveIntegerField(null=True)
    id = models.CharField(max_length=100, null=True)
    
    class Meta:
        ordering = ['rank']


    def __str__(self):
        return self.id if self.id else self.name


    def set_score(self, distribution, included_keys, total_num):
        self.score = 0
        def calc_score(trait, option):
            num_with_trait = distribution[trait][option]
            trait_score = 1 / (num_with_trait / total_num)
            self.score += trait_score


        metadata = self.onchain_metadata
        for key in included_keys:
            value = metadata.get(key, None)
            if type(value) is list:
                for elm in value:
                    calc_score(key, elm)
            else:
                calc_score(key, value)
        self.save()


    def set_id(self):
        bytes_obj = bytes.fromhex(self.name)
        self.id = bytes_obj.decode('ASCII')
        self.save()
