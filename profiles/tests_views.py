""" TESTS FOR PROFILES VIEWS """

from django.test import TestCase, Client
from django.contrib.auth.models import User


class ProductionViewTest(TestCase):
    """ Test profile views """
    
    fixtures = ["testdbdata.json"]

    def setUp(self):
        self.client = Client()


    def test_profile_view(self):
        """ Test profile view works """
        logged_user = self.client.login(username='tom', password='valid_password1')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_comment_edit_view(self):
        """ Test profile view works """
        logged_user = self.client.login(username='tom', password='valid_password1')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
