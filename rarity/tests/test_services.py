from django.test import TestCase
from django.core.exceptions import ValidationError
from rarity.services import fetch_num_pages, validate_policy_id

class ServicesTest(TestCase):
    def test_fetch_num_pages(self):
        policy_id = '7a5a5c3757d33c2b2ff0b09405676e61f93d28b5d12805dd3320e31f'
        num_pages = fetch_num_pages(policy_id)
        self.assertEqual(num_pages, 100)