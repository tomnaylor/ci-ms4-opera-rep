""" TESTS FOR PROFILES VIEWS """

from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User


class DonationViewTest(TestCase):
    """ Donations views """

    def setUp(self):
        self.client = Client()


    def test_new_donation_view(self):
        """ Test a new donation view works """
        response = self.client.get('/donations/?donation_total=10')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/donation.html')
