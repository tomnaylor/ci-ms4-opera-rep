""" Views for all donations """

import stripe
from django.shortcuts import (
                              render,
                              get_object_or_404,
                              redirect,
                              reverse,
                              HttpResponse)
from django.contrib import messages
from django.views.decorators.http import require_POST

from profiles.models import UserProfile
from works.models import Production
from profiles.forms import UserProfileForm
from django.conf import settings

from .models import Donation
from .forms import DonationForm


@require_POST
def cache_checkout_data(request):
    """
    Try stripe payment, submitted via JS from donation form.
    Updates the payment intent and return 200 if ok.
    """
    try:
        # Get and format the client secret
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Modify the payment intent from Stripe
        stripe.PaymentIntent.modify(pid, metadata={
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })

        return HttpResponse(status=200)

    except Exception as error:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=error, status=400)


def donation(request):
    """
    Display the donation form and initial payment intent
    Taken inspiration from the CI course
    """

    # Get stripe keys from settings
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Fail if no key
    if not stripe_public_key:
        messages.warning(request, ('Stripe public key is missing. '
                                   'Did you forget to set it in '
                                   'your environment?'))

    stripe.api_key = stripe_secret_key

    if request.method == 'POST':

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'country': request.POST['country'],
            'city': request.POST['city'],
            'production': request.POST['production'],
        }

        donation_form = DonationForm(form_data)

        if donation_form.is_valid():
            # Pause saving the donation form
            donation = donation_form.save(commit=False)

            # Get Client secret and add to stripe intent
            pid = request.POST.get('client_secret').split('_secret')[0]
            donation.stripe_pid = pid

            stripe_intent = stripe.PaymentIntent.retrieve(pid)

            # Set donation amount into pence
            donation.donation_total = float(stripe_intent.amount)/100

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

    # Attempt to prefill the form from user profile

    if 'donation_total' in request.GET:
        donation_total = request.GET['donation_total']
    else:
        donation_total = 10

    if 'production' in request.GET:
        production = get_object_or_404(
            Production, id=request.GET['production'])
    else:
        production = False

    # If its a logged in user
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

    # Try the stripe initial payment intent
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(float(donation_total)*100),
            currency=settings.STRIPE_CURRENCY,
        )
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=500)

    context = {
        'production': production,
        'donation_form': donation_form,
        'donation_total': donation_total,
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

    # If user is logged in, update info if requested
    # Taken inspiration from the CI course
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
