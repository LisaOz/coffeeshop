from django.urls import path
from . import views

# Create URLs patterns for product catalog: product_list and product_detail

# Staff-related URLs
app_name = 'shop'
urlpatterns = [
    path('staff/', views.staff_roles, name='staff_roles'),
    path('staff/<slug:role_slug>/', views.staff_role_detail, name='staff_role_detail'),
    path('barista/', views.barista_dashboard, name='barista_dashboard'),

    # Product-related URLs
    path('', views.product_list, name='product_list'),
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