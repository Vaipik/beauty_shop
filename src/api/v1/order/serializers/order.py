from rest_framework import serializers

from core.order.models import Order
from .item import OrderItemSerializer


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer that used for Orders."""

    items = OrderItemSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id"]
