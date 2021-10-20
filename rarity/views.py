from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Project, Collection, Asset
from .serializers import AssetSerializer, CollectionSerializer, ProjectSerializer
import json, logging

logger = logging.getLogger(__name__)

# Views
def assets(request):
    return render(request, 'assets.html')

# API Endpoints
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionSerializer

    def get_queryset(self):
        queryset = Collection.objects.all()
        project = self.request.query_params.get('project')
        if project is not None:
            queryset = queryset.filter(project__query_name=project)
        return queryset


class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AssetSerializer

    def get_queryset(self):
        queryset = Asset.objects.all()
        policy_id = self.request.query_params.get('policy_id')
        tags = self.request.query_params.get('query_obj')
        serial = self.request.query_params.get('serial')
        if policy_id is not None:
            queryset = queryset.filter(policy_id=policy_id)
        if serial:
           result = queryset.filter(serial=int(serial.lstrip('0')))
           if result: return result
        if tags:
            tags = json.loads(tags)
            for tag in tags:
                key, value = list(tag.items())[0]
                value = None if value == 'null' else value
                if type(value) is list:
                    queryset = queryset.filter(onchain_metadata__contains=tag)
                else:
                    filtering = {f'onchain_metadata__{key}': value}
                    queryset = queryset.filter(**filtering)
        return queryset
