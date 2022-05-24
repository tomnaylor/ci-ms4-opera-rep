import uuid
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from works.models import Production


class Donation(models.Model):
    """ Donation model """

    donation_number = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    production = models.ForeignKey(Production, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    # phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False, default="GB")
    # postcode = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    # street_address1 = models.CharField(max_length=80, null=False, blank=False)
    # street_address2 = models.CharField(max_length=80, null=True, blank=True)

    record_added = models.DateTimeField(auto_now_add=True)
    record_edited = models.DateTimeField(auto_now=True)

    donation_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def __str__(self):
        return str(self.donation_number)

