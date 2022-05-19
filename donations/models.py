import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django_countries.fields import CountryField
from profiles.models import UserProfile


class Donation(models.Model):
    """ Donation model """

    donation_number = models.CharField(max_length=32, null=False, editable=True, default=uuid.uuid4().hex.upper())
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False, default="GB")
    postcode = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)

    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    donation_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')


    # def generate_donation_number(self):
    #     """
    #     Generate a random, unique order number using UUID
    #     """
    #     return uuid.uuid4().hex.upper()


    # def save(self, *args, **kwargs):
    #     """
    #     Override the original save method to set the order number
    #     if it hasn't been set already.
    #     """
    #     if not self.donation_number:
    #         self.donation_number = self.generate_donation_number()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.donation_number

