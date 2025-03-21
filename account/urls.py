
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = 'account'  # define the namespace

urlpatterns = [

    # Django-provided authentication framework views:

    path('account_details/', views.account_details, name='account_details'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.user_register, name='register'),
    #path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),


]