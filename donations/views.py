from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from .models import Donation
from .forms import DonationForm


def donation(request):
    """ Display the user's profile. """

    form = DonationForm()

 
    context = {
        'form': form,
        'stripe_public_key': 'pk_test_51KSTcAIIeVztxuCKTab70ueu2539Q8vqDnIEkxrVPVVU2FcfxPjUGSsFlthKpycWl6EdCzmIVENzcTBmJmzP2S5j00Hv7lW0xc',
        'client_secret': 'xxx'

    }

    return render(request, 'donations/donation.html', context)
