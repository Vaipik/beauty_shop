from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from utils.phone import is_phone_number_valid
from core.order.models import Order
from api.v1.order import services
from .item import OrderItemSerializer


User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    """Serializer that used for Orders."""

    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    isPaid = serializers.BooleanField(source="is_paid", read_only=True)
    userId = serializers.PrimaryKeyRelatedField(
        source="user_id", queryset=User.objects.all()
    )
    items = OrderItemSerializer(many=True, read_only=False)

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
            "userId",
            "items",
        ]
        read_only_fields = ["id", "status", "isPaid"]

    def create(self, validated_data) -> Order:
        """Create a new order with nested order items."""
        items = validated_data.pop("items")
        order = services.create_order(items, validated_data)
        return order

    def validate_phone(self, phone: str) -> str:
        """Perfrom a validation using regex. Raise error if it is not valid."""
        if len(phone) != 10:
            raise serializers.ValidationError(
                detail="Must be 10 digits.",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if not is_phone_number_valid(phone):
            raise serializers.ValidationError(
                detail="Must be valid mobile number.",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return phone
