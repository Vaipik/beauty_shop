from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.v1.product.serializers import ProductSerializer
from core.cart.models.cart import ShoppingCart, CartItem


User = get_user_model()


class CartItemSerializer(serializers.ModelSerializer):
    """serializer used for items in the cart."""

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "price", "cost"]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer used for сart."""

    cartitem_set = CartItemSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ["id", "user", "total_quantity", "total_price", "cartitem_set"]
        read_only_fields = ["id", "user", "total_quantity", "total_price"]
