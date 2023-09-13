from rest_framework import serializers

from core.order.models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order item(s) that is(are) presented in user cart."""

    orderID = serializers.UUIDField(read_only=True, source="order_id")
    productID = serializers.UUIDField(required=True, source="product_id")

    class Meta:
        model = OrderItem
        fields = ["id", "price", "quantity", "orderID", "productID", "cost"]
        read_only_fields = ["id", "price", "order"]
