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
    # retrieve current Order object ID with order_id session key, stored before with order_create view
    order_id = request.session.get('order_id')
    if not order_id:
        print("Debug: no order_id in session") # debug log
        return redirect('payment:canceled')  # Redirect to a page indicating something went wrong or no order exists

    order = get_object_or_404(Order, id=order_id)  # Order obj for the given ID retrieved. Exception if no order found
    print(f"Debug: Found order {order.id}")  # Debug log
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

        # Add order items to the checkout session before  creating the Stripe session
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),  # unit is the smallest amount used for payment
                        'currency': 'GBP',  # three letters in ISO format: Great Britain Pound
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                }
            )
        # Create the Stripe checkout session
        try:
            checkout_session = stripe.checkout.Session.create(**session_data)

            # Redirect to Stripe checkout session
            return redirect(checkout_session.url)  # Redirect to the Stripe checkout page

        except stripe.error.StripeError as e:
            print(f"Stripe Error: {e}")  # Debug log
            # Handle Stripe API errors (e.g., invalid request, etc.)
            return render(request, 'payment/cancelled.html', {'error': str(e)})

    return render(request, 'payment/process.html', locals())


"""
View for the payment success
"""


def payment_completed(request):
    return render(request, 'payment/completed.html')


"""
View for the canceled payment
"""


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
