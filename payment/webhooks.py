import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order

"""
Method to verify the signature and construct the event from the JSON payload
"""


@csrf_exempt  # decorator is used to prevent Django from performing csrf validation done on all POST requests
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(  # this method is used to verify the event's signature header
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)  # if the event's payload of the signature is invalid
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)  # If the signature is invalid/ Bad Request Response

    """
    Actions done on the webhook endpoint
    ....................................
    Method to check whether the event received is checkout.session.completed. 
    This event indicates that the checkout session has been completed successfully.
    if this event is received, the session object is retrieved and checked if the session mode is payment (one-off)
    """
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if (
            session.mode == 'payment' and session.payment_status == 'paid'
        ):
            # Check whether the session mode is payment
            try:
                order = Order.objects.get(
                    id=session.client_reference_id
                    # Use client_reference_id attribute used when checkout session was created,
                    # and use Django OMR to retrieve the order object with the given id
                )
            except Order.DoesNotExist:
                return HttpResponse(status=404)  # if the order does not exist

            order.paid = True  # Mark order as paid
            order.stripe_id = session.payment_intent  # Store payment intent ID in the stripe_id field of the Order
            order.save()  # Save the order in the database

    return HttpResponse(status=200)  # All is OK
