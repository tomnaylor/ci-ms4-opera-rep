from django.urls import reverse
from django.test import TestCase, Client


class HomeViewTest(TestCase):
    """ Tests for the home page """
    def setUp(self):
        self.client = Client()
        self.url = reverse("home")

    def test_home_response_success(self):
        """ Test home page is correct """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the WNO")
