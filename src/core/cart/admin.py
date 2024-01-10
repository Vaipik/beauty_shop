from django.contrib import admin

from core.cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 2


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = (
        "id",
        "user",
        "total_quantity",
        "total_price",
        "created_at",
        "updated_at",
        "is_active",
    )


class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "quantity",
        "price",
        "cost",
    )


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
