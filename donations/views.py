""" Views for all donations """

import json
import stripe
from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from profiles.models import UserProfile
from works.models import Production
from profiles.forms import UserProfileForm
from django.conf import settings

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
            'country': request.POST['country'],
            'city': request.POST['city'],
            'donation_total': request.POST['donation_total'],
            'production': request.POST['production'],
        }

        donation_form = DonationForm(form_data)

        if donation_form.is_valid():
            donation = donation_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            donation.stripe_pid = pid

            # Save the user to the form
            if request.user.is_authenticated:
                donation.user = request.user

            donation.save()

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('donation_success',
                                    args=[donation.donation_number]))
        else:
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))
    else:

        # Attempt to prefill the form with any info
        # the user maintains in their profile

        if 'donation_total' in request.GET:
            donation_total = request.GET['donation_total']
        else:
            donation_total = 10

        if 'production' in request.GET:
            production = get_object_or_404(Production, id=request.GET['production'])
        else:
            production = False

        if request.user.is_authenticated:
            try:
                profile = get_object_or_404(UserProfile, user=request.user)
                donation_form = DonationForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'country': profile.country,
                    'city': profile.city,
                    'donation_total': donation_total,
                    'production': production,
                })

            except UserProfile.DoesNotExist:
                donation_form = DonationForm(initial={
                    'donation_total': donation_total,
                    'production': production,
                })
        else:
            donation_form = DonationForm(initial={
                'donation_total': donation_total,
                'production': production,
            })

    if not stripe_public_key:
        messages.warning(request, ('Stripe public key is missing. '
                                   'Did you forget to set it in '
                                   'your environment?'))

    stripe.api_key = stripe_secret_key
    try:
        intent = stripe.PaymentIntent.create(
            amount=30,
            currency=settings.STRIPE_CURRENCY,
        )
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=500)
        #return HttpResponse(content=e, status=500)



    context = {
        'production': production,
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
        
        # Save the user's info
        if save_info:
            profile_data = {
                'country': donation.country,
                'city': donation.city,
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
