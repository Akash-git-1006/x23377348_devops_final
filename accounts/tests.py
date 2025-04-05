from django.test import TestCase

# Create your tests here.
from django.urls import reverse

class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))  # Make sure 'home' matches your URL name
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'accounts/index.html')
