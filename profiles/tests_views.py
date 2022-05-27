""" TESTS FOR PROFILES VIEWS """

from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserComment


class ProductionViewTest(TestCase):
    """ Test profile views """

    fixtures = ["testdbdata.json"]

    def setUp(self):
        self.client = Client()

    # Profile view (logged in and out)

    def test_profile_view(self):
        """ Test profile view works """
        logged_user = self.client.login(username='tom', password='valid_password1')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_view_no_user_view(self):
        """ Test profile view delete comment with no user """
        response = self.client.get('/profile/')
        self.assertRedirects(
                             response,
                             '/accounts/login/?next=/profile/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    # Comment edit (logged in and out)

    def test_profile_comment_edit_no_user_view(self):
        """ Test profile comment edit view no user fails """
        response = self.client.get('/profile/comment-edit/1/')
        self.assertRedirects(
                             response,
                             '/accounts/login/?next=/profile/comment-edit/1/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_profile_comment_edit_view(self):
        """ Test profile comment edit view no user fails """
        logged_user = self.client.login(username='tom', password='valid_password1')
        response = self.client.get('/profile/comment-edit/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/comment-edit.html')
        self.assertContains(response, "Test comment one text")

    def test_profile_comment_edit_other_user_fail_view(self):
        """ Test profile comment edit another users comment fails """
        logged_user = self.client.login(username='notadmin', password='valid_password1')
        response = self.client.get('/profile/comment-edit/1/')
        self.assertRedirects(
                             response,
                             '/works/productions/migrations-2022',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    # Comment delete (logged in and out)

    def test_profile_comment_del_no_user_view(self):
        """ Test profile comment del view no user fails """
        response = self.client.get('/profile/comment-delete/1/')
        self.assertRedirects(
                             response,
                             '/accounts/login/?next=/profile/comment-delete/1/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_profile_comment_del_view(self):
        """ Test profile comment del view no user fails """
        logged_user = self.client.login(username='tom', password='valid_password1')
        response = self.client.get('/profile/comment-delete/1/')
        self.assertRedirects(
                             response,
                             '/works/productions/migrations-2022',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_profile_comment_del_other_user_fail_view(self):
        """ Test profile comment del another users comment fails """
        logged_user = self.client.login(username='notadmin', password='valid_password1')
        response = self.client.get('/profile/comment-delete/1/')
        self.assertRedirects(
                             response,
                             '/works/productions/migrations-2022',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)
    # ADD A TEST FOR NOT YOUR POST FAIL

    # Comment add (logged in and out)

    def test_profile_comment_add_no_user_view(self):
        """ Test profile comment add view no user fails """
        response = self.client.post('/profile/comment-add/1/',
                                    {
                                     'comment': 'Test comment one'})
        self.assertRedirects(
                             response,
                             '/accounts/login/?next=/profile/comment-add/1/',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_profile_comment_add_view(self):
        """ Test profile comment add view """
        logged_user = self.client.login(username='tom', password='valid_password1')
        response = self.client.post('/profile/comment-add/2/', 
                                    {
                                     'comment': 'Test comment one'})
        self.assertRedirects(
                             response,
                             '/works/productions/madam-butterfly-2021',
                             status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)