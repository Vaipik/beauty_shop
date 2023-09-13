from rest_framework import serializers

from core.order.models import Order
from api.v1.order import services
from .item import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Serializer that used for Orders."""

    items = OrderItemSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id"]

    def create(self, validated_data) -> Order:
        """Create a new order with nested order items."""
        items = validated_data.pop("items")
        order = services.create_order(items, validated_data)
        return order
