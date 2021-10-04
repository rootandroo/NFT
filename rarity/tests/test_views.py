from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework import status
from rarity.tests.test_models import CollectionTest
from rarity import views
import json

class AssetsViewTest(TestCase):
    def test_url_exists(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_url_by_name(self):
        response = self.client.get(reverse('assets'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('assets'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assets.html')


class CollectionViewSet(APITestCase):
    list_url = reverse('collection-list')

    @classmethod
    def setUp(self):
        self.user = User.objects.create(username='admin')

    def test_collection(self):
        factory = APIRequestFactory()
        view = views.CollectionViewSet.as_view({'get':'list'})
        
        request = factory.get(reverse('collection-list'), format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_collection_filter_by_project(self):
        factory = APIRequestFactory()
        view = views.CollectionViewSet.as_view({'get': 'list'})
        request = factory.get(reverse('collection-list'), {'project': 'CryptoDino'})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AssetViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin')
        self.policy_id = '7a5a5c3757d33c2b2ff0b09405676e61f93d28b5d12805dd3320e31f'
        self.project = 'CryptoDino'
        CollectionTest.create_collection(self, name=self.project, policy_id=self.policy_id)        

    def test_asset(self):
        factory = APIRequestFactory()
        view = views.AssetViewSet.as_view({'get': 'list'})
        request = factory.get(reverse('asset-list'))
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_asset_filter_by_policy(self):
        factory = APIRequestFactory()
        view = views.AssetViewSet.as_view({'get': 'list'})
        request = factory.get(reverse('asset-list'), {'policy_id': self.policy_id})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(json.dumps(response.data))['results']
        self.assertEqual(results[0]['policy_id'], self.policy_id)

    def test_asset_filter_by_tags(self):
        factory = APIRequestFactory()
        view = views.AssetViewSet.as_view({'get': 'list'})
        request = factory.get(
            reverse('asset-list'), { 
                "policy_id": self.policy_id,
                "query_obj": '{"attributes_body": "white"}' })
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(json.dumps(response.data))['results']
        self.assertEqual(results[0]["onchain_metadata"]['attributes_body'], 'white')