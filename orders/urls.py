from django.urls import path
from . import views


"""
URL pattern for the order_create view
"""
app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path(
        'admin/order/<int:order_id>/',
        views.admin_order_detail,
        name='admin_order_detail'
    ),
    path('admin/order/<int:order_id>/pdf/',
         views.admin_order_pdf,
         name='admin_order_pdf'
    ),

    # path('completed/', views.payment_completed, name='payment_completed'),
    path('payment/completed/', views.payment_completed, name='payment_completed'),  # Path to the payment completion
    path('barista/', views.barista_dashboard, name='barista_dashboard'),
    path('order/preparing/<int:order_id>/', views.mark_order_preparing, name='mark_order_preparing'),
    path('order/collected/<int:order_id>/', views.mark_order_collected, name='mark_order_collected'),

]

