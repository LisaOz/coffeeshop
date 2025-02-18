from django.urls import path
from . import views


"""
URL pattern for the order_create view
"""
app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path(
        'admin/order/<int:order_id>',
        views.admin_order_detail,
        name='admin_order_detail'
    ),
]
