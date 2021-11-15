from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Project, Collection, Asset
from .serializers import AssetSerializer, CollectionSerializer, ProjectSerializer
import json, logging

logger = logging.getLogger(__name__)

# Views
def assets(request, project=None, drop=None):
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
        rank_filter = self.request.query_params.get('rank_filter')
        price_filter = self.request.query_params.get('price_filter')

        if policy_id is not None:
            queryset = queryset.filter(policy_id=policy_id)

        if serial:
           result = queryset.filter(serial=int(serial.lstrip('0')))
           if result: return result

        if rank_filter:
            rank_filter = json.loads(rank_filter)
            min, max = (rank_filter["min"], rank_filter["max"])
            if min: queryset = queryset.filter(rank__gte=min)
            if max: queryset = queryset.filter(rank__lte=max)
            
        if price_filter:
            price_filter = json.loads(price_filter)
            min, max = (price_filter["min"], price_filter["max"])
            if min: queryset = queryset.filter(market__CNFTio__price__gte=min * 1_000_000)
            if max: queryset = queryset.filter(market__CNFTio__price__lte=max * 1_000_000)

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
