"""
This file contains URL patterns for views to add, remove, update and display of the items in the cart
"""

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),  # Route for viewing the details of the shopping cart
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),  # Route for adding a product to the cart
    path(
        'remove/<int:product_id>/',  # Route for removing a product from the cart
        views.cart_remove,
        name='cart_remove'
    ),
]