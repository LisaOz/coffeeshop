from django.urls import path
from . import views, webhooks

app_name = "payment"

"""
URLs for the payments workflow
"""
urlpatterns = [
    # view to display the order summary, create Stripe checkout session, and redirect to the Stripe-hosted payment form
    path('process/', views.payment_process, name='process'),

    # view for Stripe to redirect the user if the payment is successful
    path('completed/', views.payment_completed, name='completed'),

    # view for Stripe to redirect the user if the payment is cancelled
    path('canceled/', views.payment_canceled, name='canceled'),

    # URL pattern for the Stripe webhook
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
    path('completed/', views.payment_completed, name='payment_completed'),

]