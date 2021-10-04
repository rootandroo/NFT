from django.test import TestCase
from rarity.models import *

class ProjectTest(TestCase):
    def create_project(self, name='Test'):
        return Project(name=name)

    def test_project_str(self):
        project = self.create_project(name='CryptoDino')
        self.assertEqual(str(project), project.name)


class CollectionTest(TestCase):
    def create_collection(self, policy_id='blank', name='blank'):
        project = ProjectTest.create_project(ProjectTest, name=name)
        project.save()
        collection = Collection(policy_id=policy_id, project=project)
        collection.num_pages = 1
        collection.save()
        return collection

    def test_collection_str(self):
        policy_id = '7a5a5c3757d33c2b2ff0b09405676e61f93d28b5d12805dd3320e31f'
        name= 'CryptoDino'
        collection = self.create_collection(policy_id=policy_id, name=name)
        self.assertEqual(str(collection), name)

