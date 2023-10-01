from rest_framework import serializers


class TimeStampedSerializer(serializers.ModelSerializer):
    """Serializer that transofrm snake_case into camelCase for timestamp fields."""

    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
