from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from django.conf import settings

import stripe
import json

from .models import Donation
from .forms import DonationForm




@require_POST
def cache_checkout_data(request):
    """ Try stripe payment """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)


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


def donation_success(request, donation_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    donation = get_object_or_404(Donation, donation_number=donation_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        donation.user_profile = profile
        donation.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': donation.phone_number,
                'default_country': donation.country,
                'default_postcode': donation.postcode,
                'default_city': donation.city,
                'default_street_address1': donation.street_address1,
                'default_street_address2': donation.street_address2,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Donation successfully processed! \
        Your donation number is {donation_number}. A confirmation \
        email will be sent to {donation.email}.')

    context = {
        'donation': donation,
    }

    return render(request, 'donations/success.html', context)
