from django.test import TestCase

from rarity.forms import PopulateForm
from rarity.models import Project, Collection


class PopulateFormTest(TestCase):
    def test_invalid_policy_id(self):
        form = PopulateForm(data={
            'name': 'CryptoDino', 
            'policy_id': 'Invalid'})
        self.assertFalse(form.is_valid())

    def test_valid_policy_id(self):
        form = PopulateForm({
            'name': 'CryptoDino',
            'policy_id': '7a5a5c3757d33c2b2ff0b09405676e61f93d28b5d12805dd3320e31f'
        })
        self.assertTrue(form.is_valid())

    def test_duplicate_policy_id(self):
        name = 'CryptoDino'
        policy_id = '7a5a5c3757d33c2b2ff0b09405676e61f93d28b5d12805dd3320e31f'

        project = Project.objects.create(name=name)
        project.save()
        
        collection = Collection.objects.create(
            policy_id=policy_id, 
            project=project)
        collection.save()
        
        form = PopulateForm({
            'name': name,
            'policy_id': policy_id
        })
        self.assertFalse(form.is_valid())



        