""" TEST FOR SETTINGS """

from django.test import TestCase
from django.conf import settings


class SettingsTestCase(TestCase):
    """ Test settings are set """

    def test_login_url(self):
        """ Test for login URL """
        self.assertEqual(settings.LOGIN_URL, "/accounts/login/")

    def test_redirect_url(self):
        """ Test for redirect URL """
        self.assertEqual(settings.LOGIN_REDIRECT_URL, "/")

    def test_logout_redirect_url(self):
        """ Test for logout URL """
        self.assertEqual(settings.LOGOUT_REDIRECT_URL, "/")
