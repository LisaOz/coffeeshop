from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe


# Register your models here.


# Method to add a link to each Order object on the list page of the admin site.
# It takes an Order object as an argument and returns an HTML link with the payment URL in Stripe

def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)  # here use 'mark-safe avoid auto-escape. Don't use on the inputs coming from the users!!
    return ""


order_payment.short_description = "Stripe payment"

"""
OrderInLine class is created to include the OrderItem model on the same edit page with its model
"""


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        order_payment,
        "created",
        "updated"
    ]

    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
