from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    twitter = models.URLField(max_length=23, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Collection(models.Model):
    # property_keys, strings for accessing metadata, strings surrounded by [] map to lists
    policy_id = models.CharField(max_length=56, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collections')
    property_keys = models.JSONField(null=True)

    class Meta:
        ordering = ['project']

    def __str__(self):
        return f'{self.project}: {self.property_keys}'
    
    @property
    def distribution(self):
        "Returns a dictionary mapping key:value pairs to their frequency."
        if self.property_keys is None:
            return None

        def parse_object(key, object): 
            if type(object) is list:
                for element in object:
                    parse_object(key, element)
            else:
                if key in res:
                    res[key][object] = res[key].get(object, 0) + 1
                else: 
                    res[key] = {}
                    res[key][object] = 1               

        res = {}
        assets = self.assets.all()
        for key in self.property_keys:
            for asset in assets:
                metadata = asset.onchain_metadata
                if metadata:
                    parse_object(key, metadata.get(key))               
        return res


class Asset(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    policy_id = models.CharField(max_length=56)
    fingerprint = models.CharField(max_length=44, unique=True)
    quantity = models.PositiveBigIntegerField()
    mint_tx_hash = models.CharField(max_length=64)
    onchain_metadata = models.JSONField(null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='assets')
    
    @property
    def ascii_name(self):
        bytes_obj = bytes.fromhex(self.name)
        return bytes_obj.decode('ASCII')
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.ascii_name


