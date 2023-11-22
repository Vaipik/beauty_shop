from django.contrib import admin
from core.cart.models.cart import *


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 2


class ShoppingCartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = (
        "id",
        "user",
        "total_quantity",
        "total_price",
        "created_at",
        "updated_at",
    )


class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "quantity",
        "price",
        "cost",
        "created_at",
        "updated_at",
    )


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(CartItem, CartItemAdmin)
