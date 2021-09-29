from .models import Project, Collection, Asset
from rest_framework import serializers
        

class ProjectSerializer(serializers.ModelSerializer):
    collections = serializers.StringRelatedField(many=True)
    class Meta:
        model = Project
        fields = ['name', 'twitter', 'collections']


class CollectionSerializer(serializers.ModelSerializer):
    distribution = serializers.JSONField()
    class Meta:
        model = Collection
        fields = ['policy_id', 'project', 'property_keys', 'distribution']
        # TODO
        # Optionally exclude some fields when sending API requests

class AssetSerializer(serializers.ModelSerializer):
    onchain_metadata = serializers.JSONField(allow_null=True)
    class Meta:
        model = Asset
        fields = ['name', 'policy_id', 'fingerprint', 'quantity', 'mint_tx_hash', 'onchain_metadata'] 


