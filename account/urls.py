from django.contrib.auth import views as auth_views
from django.urls import path

import orders
from . import views
from orders.views import barista_dashboard
from django.contrib.auth import views as auth_views

app_name = 'account'  # define the namespace

# Django-provided authentication framework views:

urlpatterns = [
    # Existing URLs
    path('account_details/', views.account_details, name='account_details'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password reset views

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Custom views
    path('register/', views.user_register, name='register'),
    path('orders/barista_dashboard/', orders.views.barista_dashboard, name='barista_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('staff_logout/', views.staff_logout, name='staff_logout'),
]
