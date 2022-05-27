"""
Webhook function modified from Stripes developer documents
"""

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from donations.stripe_webhook_class import StripeHandler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """ Webhook for Stripe confirmations """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    wh_secret = settings.STRIPE_WH_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as error:
        # Invalid payload
        raise error
    except stripe.error.SignatureVerificationError as error:
        # Invalid signature
        raise error

    # Handle the event
    handler = StripeHandler(request)

    if event['type'] == 'payment_intent.payment_failed':
        handler.handle_payment_intent_payment_failed(event)
    elif event['type'] == 'payment_intent.succeeded':
        handler.handle_payment_intent_succeeded(event)
    else:
        print(f'Unhandled event type { format(event.type) }')

    return HttpResponse(status=200)
