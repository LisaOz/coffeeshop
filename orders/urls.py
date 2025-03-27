from django.urls import path
from . import views


"""
URL pattern for the order_create view
"""
app_name = 'orders'

urlpatterns = [
 # Order creation and payment
    path('create/', views.order_create, name='order_create'),
    path('created/', views.order_created, name='order_created'),
    path('order/<int:order_id>/detail/', views.admin_order_detail, name='admin_order_detail'),
    path(
        'admin/order/<int:order_id>/',
        views.admin_order_detail,
        name='admin_order_detail'
    ),
    path('admin/order/<int:order_id>/pdf/',
         views.admin_order_pdf,
         name='admin_order_pdf'
    ),

    path('payment/completed/', views.payment_completed, name='payment_completed'),  # Path to the payment completion



    # Order status updates for Baristas
    path('barista-dashboard/', views.barista_dashboard, name='barista_dashboard'),

    # URL for marking an order as 'Preparing'
    path('mark-order-preparing/<int:order_id>/', views.mark_order_preparing, name='mark_order_preparing'),

    # URL for marking an order as 'Collected'
    path('mark-order-collected/<int:order_id>/', views.mark_order_collected, name='mark_order_collected'),

    # URL for marking an order as 'Pending' (default state)
    path('mark-order-pending/<int:order_id>/', views.update_order_status, name='mark_order_pending'),
]