from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Donation
from profiles.models import UserProfile

import json
import time


class StripeHandler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, donation):
        """Send the user a confirmation email"""
        cust_email = donation.email
        subject = render_to_string(
            'donations/emails/success-subject.txt',
            {'donation': donation})
        body = render_to_string(
            'donations/emails/success-body.txt',
            {'donation': donation, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        # shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.country = billing_details.address.country
                profile.city = billing_details.address.city
                profile.save()

        donation_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                donation = Donation.objects.get(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    country__iexact=billing_details.address.country,
                    city__iexact=billing_details.address.city,
                    donation_total=grand_total,
                    stripe_pid=pid,
                )
                donation_exists = True
                break
            except Donation.DoesNotExist:
                attempt += 1
                time.sleep(1)
        
        if donation_exists:
            self._send_confirmation_email(donation)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified donation already in database'),
                status=200)
        else:
            donation = None
            try:
                donation = Donation.objects.create(
                    user_profile=profile,
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    country__iexact=billing_details.address.country,
                    city__iexact=billing_details.address.city,
                    donation_total=grand_total,
                    stripe_pid=pid,
                )
            except Exception as error:
                if donation:
                    donation.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {error}',
                    status=500)
        self._send_confirmation_email(donation)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created order in webhook'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
