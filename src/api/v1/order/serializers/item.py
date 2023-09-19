from rest_framework import serializers

from api.v1.order import services
from core.order.models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Order items that are presented in user cart. GET method."""

    orderID = serializers.UUIDField(read_only=True, source="order_id")
    productID = serializers.UUIDField(required=True, source="product_id")

    class Meta:
        model = OrderItem
        fields = ["id", "price", "quantity", "orderID", "productID", "cost"]
        read_only_fields = ["id", "price", "cost"]


class OrderItemUpdateOrCreateSerializer(OrderItemSerializer):
    """Update or create order item for existing order."""

    orderID = serializers.UUIDField(source="order_id")

    def create(self, validated_data) -> OrderItem:
        """Create an order item for existing order."""
        return services.create_order_item(**validated_data)
