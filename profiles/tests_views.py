""" TESTS FOR PROFILES VIEWS """

from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User


class ProductionViewTest(TestCase):
    """ Test profile views """

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

    def test_profile_view(self):
        """ Test profile view works """
        self.client.post('/accounts/login/',
                         {
                          'login': self.username,
                          'password': self.password})
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_comment_edit_view(self):
        """ Test profile view works """
        self.client.post('/accounts/login/',
                         {
                          'login': self.username,
                          'password': self.password})
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
