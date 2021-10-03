from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required


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


@staff_member_required
class PopulateViewTest(TestCase):
        def test_url_exists(self):
            response = self.client.get("populate/")
            self.assertEqual(response.status_code, 200)

        def test_url_by_name(self):
            response = self.client.get(reverse('populate'))
            self.assertEqual(response.status_code, 200)
        
        def test_view_uses_correct_template(self):
            response = self.client.get(reverse('populate'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'populate.html')

        