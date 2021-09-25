from .models import Project, Collection, Asset
from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        

class ProjectSerializer(serializers.ModelSerializer):
    collections = serializers.StringRelatedField(many=True)
    class Meta:
        model = Project
        fields = ['name', 'twitter', 'collections']


class CollectionSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    distribution = serializers.JSONField
    class Meta:
        model = Collection
        fields = ['policy_id', 'project', 'property_keys', 'distribution']


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['name', 'policy_id', 'fingerprint', 'quantity', 'mint_tx_hash', 'onchain_metadata'] 


