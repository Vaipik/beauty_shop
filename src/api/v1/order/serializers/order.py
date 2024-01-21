from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from api.base.serializers import TimeStampedSerializer
from api.v1.order import services
from core.order.models import Order
from utils.phone import is_phone_number_valid

from .item import OrderItemSerializer


User = get_user_model()


class OrderSerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Serializer that used for Orders."""

    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    isPaid = serializers.BooleanField(source="is_paid")
    userId = serializers.UUIDField(source="user_id")
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "firstName",
            "lastName",
            "email",
            "phone",
            "status",
            "isPaid",
            "address",
            "userId",
            "items",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = ["id", "status", "isPaid"]

    def create(self, validated_data) -> Order:
        """Create a new order with nested order items."""
        items = validated_data.pop("items")
        order = services.create_order(items, validated_data)
        return order

    def validate_phone(self, phone: str) -> str:
        """Perfrom a validation using regex. Raise error if it is not valid."""
        if not is_phone_number_valid(phone):
            raise serializers.ValidationError(
                detail="Must be valid mobile number.",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return phone


class OrderUpdateSerializer(OrderSerializer):
    """Serializer for update. RO fields is only Order ID."""

    items = OrderItemSerializer(many=True)

    class Meta(OrderSerializer.Meta):
        read_only_fields = ["id"]
