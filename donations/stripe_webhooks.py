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
    print('STRIPEWH: 1')

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
        response = handler.handle_payment_intent_payment_failed(event)
    elif event['type'] == 'payment_intent.succeeded':
        response = handler.handle_payment_intent_succeeded(event)
    else:
        print(f'Unhandled event type { format(event.type) }')

    return HttpResponse(status=200)


    # """Listen for webhooks from Stripe"""
    # print('STRIPEWH: 1')
    # # Setup
    # wh_secret = settings.STRIPE_WH_SECRET
    # stripe.api_key = settings.STRIPE_SECRET_KEY

    # # Get the webhook data and verify its signature
    # payload = request.body
    # sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    # event = None

    # print('STRIPEWH: 2:' + wh_secret)

    # try:
    #     event = stripe.Webhook.construct_event(
    #         payload, sig_header, wh_secret
    #     )
    # except ValueError as e:
    #     # Invalid payload
    #     return HttpResponse(content=e, status=400)
    # except stripe.error.SignatureVerificationError as e:
    #     # Invalid signature
    #     return HttpResponse(content=e, status=400)
    # except Exception as e:
    #     return HttpResponse(content=e, status=400)

    # # Set up a webhook handler
    # handler = StripeHandler(request)
    # print('STRIPEWH: 3')

    # # Map webhook events to relevant handler functions
    # event_map = {
    #     'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
    #     'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    # }

    # # Get the webhook type from Stripe
    # event_type = event['type']

    # # If there's a handler for it, get it from the event map
    # # Use the generic one by default
    # event_handler = event_map.get(event_type, handler.handle_event)

    # # Call the event handler with the event
    # response = event_handler(event)

    # print('STRIPEWH: 4')

    # return response
