from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import Order

# Create your views here.

"""
Stripe instance created, Stripe API key and API version are set
"""
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

"""
Payment_process view
"""


def payment_process(request):
    order_id = request.session.get(
        'order_id')  # retrieve current Order object ID with order_id session key, stored before with order_create view
    order = get_object_or_404(Order,
                              id=order_id)  # Order object for the given ID is retrieved. Exception if no order found

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        )

        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )

        # Stripe checkout session data
        session_data = {
            'mode': 'payment',  # the mode of the checkout session
            'client_reference_id': order.id,  # unique reference for this payment, to match with the order
            'success_url': success_url,  # URL for Stripe to redirect the user to if the payment is successful
            'cancel_url': cancel_url,
            'line_items': []  # list that will be populated with the order items
        }

    else:
        return render(request, 'payment/process.html', locals())

