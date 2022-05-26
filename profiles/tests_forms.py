""" TESTS FOR PROFILES """

from django.urls import reverse
from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User
from .forms import UserProfileForm, ProductionCommentForm


class ProductionCommentFormTest(TestCase):
    """ Test production comment """

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

    def setUp(self):
        settings.ACCOUNT_EMAIL_VERIFICATION = 'none'
        self.username = "user"
        self.password = "valid_password1"
        self.email = "email@test.com"
        self.client = Client()
        self.new_user = User.objects.create_user(
                                username=self.username,
                                email=self.email,
                                is_active=True,
                                password=self.password)

    def test_profile_sends_user_to_login(self):
        """ Test profile link takes non-users to the signuppage """
        response = self.client.get(reverse("profile"), follow=True)
        self.assertRedirects(
                             response,
                             '/accounts/login/?next=/profile/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in")

    def test_user_has_been_saved(self):
        """ Test if user is saved correctly """
        self.assertEqual(self.new_user.username, self.username)
        self.assertEqual(self.new_user.email, self.email)
        self.assertIs(self.new_user.is_active, True)

    def test_user_login_success(self):
        """ Test if the user login is correct """
        response = self.client.post('/accounts/login/',
                                    {
                                     'login': self.username,
                                     'password': self.password})
        self.assertRedirects(
                             response,
                             '/',
                             status_code=302)

    def test_logged_in_user_can_access_profile(self):
        """ Test that a signed in user can access the profile """
        response = self.client.post('/accounts/login/',
                                    {
                                     'login': self.username,
                                     'password': self.password})
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile")

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
