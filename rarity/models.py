from django.db import connections, models

class Project(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    twitter = models.URLField(max_length=23, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Collection(models.Model):
    # property_keys are keys for accessing asset attributes
    policy_id = models.CharField(max_length=56, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collections')
    property_keys = models.JSONField(null=True)

    class Meta:
        ordering = ['project']

    def __str__(self):
        return f'{self.project}: {self.property_keys}'
    
    @property
    def distribution(self):
        # TODO Add Max Length to every Trait
        "Returns a dictionary mapping key:value pairs to their frequency."
        res = {}
        assets = self.assets.all()
        for key in self.property_keys:
            for asset in assets:
                metadata = asset.onchain_metadata
                # key maps to dictionary
                if type(metadata[key]) is dict:
                    for innerKey, value in metadata[key].items():
                        if innerKey in res:
                            res[innerKey][value] = res[innerKey].get(value, 0) + 1
                        else:
                            res[innerKey] = {}
                            res[innerKey][value] = 1
                # key maps to list
                elif type(metadata[key]) is list:
                    for value in metadata[key]:
                        if key in res:
                            res[key][value] = res[key].get(value, 0) + 1
                        else:
                            res[key] = {}
                            res[key][value] = 1
                # key maps to value
                else:
                    value = metadata[key]
                    if key in res:
                        res[key][value] = res[key].get(value, 0) + 1
                    else:
                        res[key] = {}
                        res[key][value] = 1                    
        return res


class Asset(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    num = models.PositiveBigIntegerField()
    policy_id = models.CharField(max_length=56)
    fingerprint = models.CharField(max_length=44, unique=True)
    quantity = models.PositiveBigIntegerField()
    mint_tx_hash = models.CharField(max_length=64)
    onchain_metadata = models.JSONField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='assets')
    
    @property
    def ascii_name(self):
        bytes_obj = bytes.fromhex(self.name)
        return bytes_obj.decode('ASCII')
    
    class Meta:
        ordering = ['num']

    def __str__(self):
        return self.ascii_name