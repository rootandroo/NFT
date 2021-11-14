from .models import Project, Collection, Asset
from rest_framework import serializers
        

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name']


class CollectionSerializer(serializers.ModelSerializer):
    distribution = serializers.JSONField()
    class Meta:
        model = Collection
        fields = ['policy_id', 'project', 'included_keys', 'distribution', 'name']


class AssetSerializer(serializers.ModelSerializer):
    onchain_metadata = serializers.JSONField(allow_null=True)
    class Meta:
        model = Asset
        fields = ['name', 'policy_id', 'onchain_metadata', 'score', 'rank', 'serial', 'alpha_name', 'market'] 

