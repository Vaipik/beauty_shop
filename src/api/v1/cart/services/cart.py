import decimal
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.cart.models import CartItem
from core.cart.models.cart import Cart
from core.product.models import Product

User = get_user_model()


@transaction.atomic
def update_cart(instance, items):
    """Get product, quantity and update it."""
    for item in items:
        product_id = item["product_id"]
        quantity = item["quantity"]
        try:
            cart_item = instance.items.get(product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            message = f"Product with id {product_id} does not exist in the cart."
            raise serializers.ValidationError(message)
    return instance


def create_or_add_cart_item(cart: Cart, product_id: UUID, price: decimal) -> CartItem:
    """Create a new items or update items and return it."""
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product_id=product_id, price=price
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return cart_item


def get_product_for_cart(cart: Cart, items: list[dict]):
    """Get product, its quantity, price and return it."""
    for item in items:
        product_id = item["product_id"]
        price = get_object_or_404(Product, pk=product_id).price
        create_or_add_cart_item(cart, product_id, price)


@transaction.atomic
def create_or_update_cart(items: list[dict], user: User) -> Cart:
    """Create a new Cart or update Cart and return it."""
    cart, created = Cart.objects.get_or_create(user=user, is_active=True)
    get_product_for_cart(cart, items)
    return cart


def get_detail_cart(pk: UUID) -> QuerySet[Cart]:
    """Return detailed data for a specific cart."""
    return (
        Cart.objects.prefetch_related("items")
        .select_related("user")
        .filter(pk=pk, is_active=True)
    )


def delete_cart(cart):
    """Make the cart inactive when an order is created or there are no items."""
    cart.is_active = False
    cart.save()


def check_cart(cart):
    """Сheck cart for items."""
    if cart.items.count() == 0:
        delete_cart(cart)
