from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.

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
         "created",
        "updated"
    ]

    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
