from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .forms import PopulateForm
from .models import Project, Collection, Asset
from .services import fetch_all_assets, create_asset_objs
from .serializers import AssetSerializer, CollectionSerializer, ProjectSerializer
import json

# Views
def assets(request):
    return render(request, 'assets.html')


@staff_member_required
def populate(request):
    if request.method == 'POST':
        form = PopulateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            project, created = Project.objects.get_or_create(name=data['name'])
     
            for policy_id in data['policy_id_list']:
                asset_list = fetch_all_assets(policy_id)

                collection = Collection.objects.create(policy_id=policy_id, project=project)
                collection.save()
                asset_objs = create_asset_objs(asset_list, collection)
                Asset.objects.bulk_create(asset_objs)
            
            return redirect('assets')
    else:
        form = PopulateForm()
    
    return render(request, 'populate.html', {'form': form})


# API Endpoints
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CollectionSerializer

    def get_queryset(self):
        queryset = Collection.objects.all()
        project = self.request.query_params.get('project')
        if project is not None:
            queryset = queryset.filter(project=project)
        return queryset


class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssetSerializer

    def get_queryset(self):
        queryset = Asset.objects.all()
        policy_id = self.request.query_params.get('policy_id')
        tags = self.request.query_params.get('query_obj')
        if policy_id is not None:
            queryset = queryset.filter(policy_id=policy_id)
        if tags:
            tags = json.loads(tags)
            print(tags)
            for trait, option in tags.items():
                if not type(option) is list:
                    if option.isnumeric():
                        tags[trait] = int(option)
                    elif option == 'null':
                        filtering = {f'onchain_metadata__{trait}__isnull': True}
                        return queryset.filter(**filtering)
            queryset = queryset.filter(onchain_metadata__contains=tags)
        return queryset