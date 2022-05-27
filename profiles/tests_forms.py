""" TESTS FOR PROFILES """

from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .forms import UserProfileForm, ProductionCommentForm


class ProductionCommentFormTest(TestCase):
    """ Test production comment """

    fixtures = ["testdbdata.json"]

    def test_profile_comment_fields_are_required(self):
        """ Test country is required user, production, comment"""
        form = ProductionCommentForm({'comment': None})
        self.assertFalse(form.is_valid())

    def test_profile_comment_fields_are_inc_in_form_metaclass(self):
        """ Test that only city and country are in the profile form """
        form = ProductionCommentForm()
        self.assertEqual(form.Meta.fields, ['comment'])


class ProfileFormTest(TestCase):
    """ Test Profile """

    fixtures = ["testdbdata.json"]
    
    def setUp(self):
        self.client = Client()

    def test_user_login_success(self):
        """ Test if the user login is correct """
        response = self.client.post('/accounts/login/',
                                    {
                                     'login': 'tom',
                                     'password': 'valid_password1'})
        self.assertRedirects(
                             response,
                             '/',
                             status_code=302)

    def test_profile_city_is_not_required(self):
        """ Test city is not required """
        form = UserProfileForm({'country': 'GB'})
        self.assertTrue(form.is_valid())

    def test_profile_country_is_required(self):
        """ Test country is required """
        form = UserProfileForm({'city': 'TEST'})
        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors.keys())
        self.assertEqual(form.errors['country'][0], 'This field is required.')

    def test_profile_fields_are_inc_in_form_metaclass(self):
        """ Test that only city and country are in the profile form """
        form = UserProfileForm()
        self.assertEqual(form.Meta.fields, ['city', 'country'])
