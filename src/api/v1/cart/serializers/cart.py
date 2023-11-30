import decimal
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.cart.models.cart import Cart, CartItem
from core.product.constants import PRODUCT_PRICE_MAX_DIGITS
from core.product.models import Product

User = get_user_model()


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for goods in Сart."""

    cartID = serializers.UUIDField(read_only=True, source="cart_id")
    productID = serializers.UUIDField(required=True, source="product_id")

    class Meta:
        model = CartItem
        fields = ["id", "cartID", "productID", "quantity", "price", "cost"]
        read_only_fields = ["id", "cartID", "price", "cost"]


class CartSerializer(serializers.ModelSerializer):
    """Serializer that used for Carts."""

    totalQuantity = serializers.IntegerField(source="total_quantity", read_only=True)
    totalPrice = serializers.DecimalField(
        source="total_price",
        max_digits=PRODUCT_PRICE_MAX_DIGITS,
        decimal_places=2,
        read_only=True,
    )
    userID = serializers.IntegerField(source="user_id", read_only=True)
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "userID", "items", "totalQuantity", "totalPrice"]
        read_only_fields = ["id", "userID", "totalQuantity", "totalPrice"]

    def create(self, validated_data) -> Cart:
        """Create Cart with goods. Use the POST method."""
        items = validated_data.pop("items")
        user = self.context["user"]
        cart = create_or_update_cart(items, user)
        return cart

    def update(self, instance, validated_data) -> Cart:
        """Update item in Cart. Use the PATCH method."""
        items = validated_data.pop("items")
        return update_cart(instance, items)


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


def create_or_add_cart_item(
    cart: Cart, product_id: UUID, price: decimal, quantity: int
) -> CartItem:
    """Create a new items or update items and return it."""
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product_id=product_id, price=price
    )
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()
    return cart_item


def create_cart_items(cart: Cart, items: list[dict]):
    """Get product, its quantity, price and reurn it."""
    for item in items:
        product_id = item["product_id"]
        quantity = item["quantity"]
        price = get_object_or_404(Product, pk=product_id).price
        create_or_add_cart_item(cart, product_id, price, quantity)


@transaction.atomic
def create_or_update_cart(items: list[dict], user: User) -> Cart:
    """Create a new Cart or update Cart and return it."""
    cart, created = Cart.objects.get_or_create(user=user, is_active=True)
    create_cart_items(cart, items)
    return cart
