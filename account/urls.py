
from django.contrib.auth import views as auth_views
from django.urls import path

import orders
from . import views
from orders.views import barista_dashboard


app_name = 'account'  # define the namespace

urlpatterns = [

    # Django-provided authentication framework views:

    path('account_details/', views.account_details, name='account_details'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

   # custom views:

    path('register/', views.user_register, name='register'),
    #path('barista_dashboard/', views.barista_dashboard_account, name='barista_dashboard'),
    path('account/barista_dashboard/', orders.views.barista_dashboard, name='barista_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('staff_logout/', views.staff_logout, name='staff_logout'),  # Staff logout URL


]