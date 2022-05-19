from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from .models import Donation
from .forms import DonationForm
from django.conf import settings

import stripe
import json

def donation(request):
    """ Display the user's profile. """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'city': request.POST['city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
        }

        donation_form = DonationForm(form_data)

        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            donation.stripe_pid = pid
            donation.original_bag = json.dumps(bag)
            donation.save()

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('donation_success',
                                    args=[donation.donation_number]))
        else:
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))
    else:

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=1000,
            currency=settings.STRIPE_CURRENCY,
        )

        # Attempt to prefill the form with any info
        # the user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = get_object_or_404(UserProfile, user=request.user)
                donation_form = DonationForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'city': profile.default_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                })
                print('USER PROFILE FOUND' + profile.default_phone_number)

            except UserProfile.DoesNotExist:
                donation_form = DonationForm()
        else:
            donation_form = DonationForm()

    if not stripe_public_key:
        messages.warning(request, ('Stripe public key is missing. '
                                   'Did you forget to set it in '
                                   'your environment?'))

    print("key:" + settings.STRIPE_PUBLIC_KEY)
    context = {
        'donation_form': donation_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'donations/donation.html', context)
