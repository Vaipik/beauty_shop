from rest_framework import serializers

from core.order.models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order item(s) that is(are) presented in user cart."""

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["id", "price", "order"]
