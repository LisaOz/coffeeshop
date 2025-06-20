"""
URL configuration for coffeeshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from orders.views import barista_dashboard

urlpatterns = [
    path('admin/', admin.site.urls), # url for admin site
    path('account/', include('account.urls')),  # url for login into account
    path('account/', include('django.contrib.auth.urls')),  # django-provided authentication framework
    path('orders/barista_dashboard/', barista_dashboard, name='barista_dashboard'), # url for barista dashboard
    path('cart/', include('cart.urls', namespace='cart')),  # this url is more restrictive, include it before shop.url
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),  # url pattern for the payment application
    path('', include('shop.urls', namespace='shop')),  # include URL path for the shop application
]


# To serve the uploaded media files using the development server.
# ONLY SERVE MEDIA FILES THIS WAY DURING DEVELOPMENT. NEVER SERVE STATIC FILES WITH DJANGO IN PRODUCTION
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )