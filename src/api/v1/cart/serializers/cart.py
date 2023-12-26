from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.cart.serializers.cartitem import CartItemSerializer
from api.v1.cart.services.cart import create_or_update_cart, update_cart
from core.cart.models.cart import Cart


User = get_user_model()


class CartSerializer(serializers.ModelSerializer):
    """Serializer that used for Carts."""

    totalQuantity = serializers.IntegerField(source="total_quantity", read_only=True)
    totalPrice = serializers.DecimalField(
        source="total_price",
        max_digits=10,
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
