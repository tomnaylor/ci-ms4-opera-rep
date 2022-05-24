from django import forms
from .models import Donation


class DonationForm(forms.ModelForm):
    """ Donation form """
    class Meta:
        model = Donation
        fields = ('full_name', 'email', 'city', 'country', 'production')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
