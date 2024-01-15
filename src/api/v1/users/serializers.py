import typing

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.base.serializers import TimeStampedSerializer

from api.v1.order.serializers import OrderSerializer
from api.v1.users import services


if typing.TYPE_CHECKING:
    from core.user_auth.models import User

User: User = get_user_model()


class UserSerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Base schema with upperCamelCase fields."""

    isActive = serializers.BooleanField(source="is_active", read_only=True)
    isStaff = serializers.BooleanField(source="is_staff", read_only=True)
    isSuperUser = serializers.BooleanField(source="is_superuser", read_only=True)
    lastLogin = serializers.DateTimeField(source="last_login", read_only=True)

    class Meta:
        model = User
        exclude = [
            "last_login",
            "is_active",
            "created_at",
            "updated_at",
            "is_superuser",
            "is_staff",
        ]
        read_only_fields = ["id", "email", "phone", "role"]
        write_only_fields = ["password"]


class UserCreateSerializer(UserSerializer):
    """Schema with password retype field."""

    default_error_messages = {
        "password_mismatch": _("The two password fields didn't match.")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rePassword"] = serializers.CharField(
            style={"input_type": "password"}, write_only=True
        )

    def validate(self, attrs):
        """Validate password."""
        self.fields.pop("rePassword", None)
        re_password = attrs.pop("rePassword")
        attrs = super().validate(attrs)
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")

    def create(self, validated_data) -> User:
        """Create custom user."""
        return services.create_user(validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Schema with user orders."""

    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "sex", "phone", "email", "orders"]


class UserProductFeedbackSerializer(serializers.ModelSerializer):
    """Schema to use for product feedbacks."""

    firstName = serializers.CharField(source="first_name", read_only=True)
    lastName = serializers.CharField(source="last_name", read_only=True)

    class Meta:
        model = User
        fields = ["firstName", "lastName"]
