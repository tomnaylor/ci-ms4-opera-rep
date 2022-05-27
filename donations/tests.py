""" TESTS FOR PROFILES VIEWS """

from django.test import TestCase, Client
from .models import Donation
from .forms import DonationForm


class DonationTest(TestCase):
    """ Donations views """

    fixtures = ["testdbdata.json"]

    def setUp(self):
        self.client = Client()

    def test_new_donation_view(self):
        """ Test a new donation view works """
        response = self.client.get('/donations/?donation_total=10')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donations/donation.html')

    def test_empty_donation_model(self):
        """ Test empty donation pass """
        donation = Donation.objects.create()
        self.assertTrue(isinstance(donation, Donation))

    def test_donation_model(self):
        """ Test donation pass """
        donation = Donation.objects.create(
                                            user_id=1,
                                            production_id=1,
                                            full_name='bob smith',
                                            email='email',
                                            country='county',
                                            city='City',
                                            donation_total=9.99,
                                            stripe_pid='xxxxxxxxxxxxxxxxxx',
                                            )
        self.assertTrue(isinstance(donation, Donation))
        self.assertTrue(donation.full_name == 'bob smith')

    def test_donation_form_email_fail(self):
        """ Test donation form email fail """
        form = DonationForm({
                             'full_name': 'bob smith',
                             'email': 'invalidemailaddress',
                             'country': 'GB',
                             'city': 'City'})
        self.assertFalse(form.is_valid())

    def test_donation_form_name_fail(self):
        """ Test donation form name fail """
        form = DonationForm({
                             'full_name': None,
                             'email': 'email@test.com',
                             'country': 'GB',
                             'city': 'City'})
        self.assertFalse(form.is_valid())

    def test_donation_form_country_fail(self):
        """ Test donation form country fail """
        form = DonationForm({
                             'full_name': 'Bob Smith',
                             'email': 'email@test.com',
                             'country': None,
                             'city': 'City'})
        self.assertFalse(form.is_valid())

    def test_donation_form_city_fail(self):
        """ Test donation form city fail """
        form = DonationForm({
                             'full_name': 'Bob Smith',
                             'email': 'email@test.com',
                             'country': 'GB',
                             'city': None})
        self.assertFalse(form.is_valid())

    def test_donation_form_is_valid(self):
        """ Test donation form ok """
        form = DonationForm({
                             'production': 1,
                             'full_name': 'bob smith',
                             'email': 'email@test.com',
                             'country': 'GB',
                             'city': 'City'})
        self.assertTrue(form.is_valid())

    def test_donation_form_meta_fields(self):
        """ Test donation form meta fields """
        self.assertEqual(DonationForm.Meta.fields, (
                                                    'full_name',
                                                    'email',
                                                    'city',
                                                    'country',
                                                    'production'))
