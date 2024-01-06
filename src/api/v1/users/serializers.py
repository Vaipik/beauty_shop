from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.base.serializers import TimeStampedSerializer

from api.v1.users import services

User = get_user_model()


class UserSerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Overriding default djoser user serializer."""

    isActive = serializers.BooleanField(source="is_active", read_only=True)
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
        ]
        read_only_fields = ["id", "email", "phone", "role"]
        write_only_fields = ["password"]


class UserCreateSerializer(UserSerializer):
    """Extending base serializer with password retype field."""

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