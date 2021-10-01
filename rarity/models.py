from django.db import models


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
    distribution = models.JSONField(null=True)

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
        super().save(*args, **kwargs)


    def fetch_distribution(keys, assets):
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
                parse_obj(key, metadata)                    
        return dist            


class Asset(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    policy_id = models.CharField(max_length=56)
    fingerprint = models.CharField(max_length=44, unique=True)
    quantity = models.PositiveBigIntegerField()
    mint_tx_hash = models.CharField(max_length=64)
    onchain_metadata = models.JSONField(null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='assets')
    score = models.PositiveIntegerField(null=True)    
        
    @property
    def ascii_name(self):
        bytes_obj = bytes.fromhex(self.name)
        return bytes_obj.decode('ASCII')
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.ascii_name


