from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.cart.models import CartItem

User = get_user_model()


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for goods in Сart."""

    cartID = serializers.UUIDField(read_only=True, source="cart_id")
    productID = serializers.UUIDField(required=True, source="product_id")

    class Meta:
        model = CartItem
        fields = ["id", "cartID", "productID", "quantity", "price", "cost"]
        read_only_fields = ["id", "cartID", "price", "cost"]
