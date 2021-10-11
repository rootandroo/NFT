from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Project, Collection, Asset
from .serializers import AssetSerializer, CollectionSerializer, ProjectSerializer
import json

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
            queryset = queryset.filter(project=project)
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
            return queryset.filter(id__icontains=serial)
        if tags:
            tags = json.loads(tags)
            for trait, option in tags.items():
                if not type(option) is list:
                   # if option.isnumeric():
                        # convert numeric str options to integers
                        # tags[trait] = int(option) 
                    if option == 'null':
                        # filter full null options
                        filtering = {f'onchain_metadata__{trait}__isnull': True}
                        return queryset.filter(**filtering)
            queryset = queryset.filter(onchain_metadata__contains=tags)
        return queryset
