from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "status",
        "is_paid",
        "user",
    )
    list_display_links = ("id", "first_name", "last_name")
    search_fields = ("first_name", "last_name", "status", "is_paid", "user")
    list_filter = ("first_name", "last_name", "status", "is_paid", "user")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "price",
        "quantity",
        "product",
        "order",
    )
    list_display_links = ("price", "quantity")
    search_fields = ("product.sku", "order")
    list_filter = ("product.sku", "order")
