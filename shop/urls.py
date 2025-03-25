from django.urls import path
from . import views

# Create URLs patterns for product catalog: product_list and product_detail

# Staff-related URLs
app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),


<<<<<<< HEAD

=======
    path('staff/', views.staff_roles, name='staff_roles'),
    path('staff/<slug:role_slug>/', views.staff_role_detail, name='staff_role_detail'),
    path('barista_dashboard/', views.barista_dashboard, name='barista_dashboard'),
>>>>>>> a4334d432523e81d4e867f41ae574e4a96ec2fa9

    # Product-related URLs
    path('product/', views.product_list, name='product_list'),
    path(
        '<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category'
    ),
    path(
        '<int:id>/<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),

]