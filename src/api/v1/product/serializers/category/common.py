from rest_framework import serializers


class ProductCategorySerializer(serializers.Serializer):
    """Serializer for `Option` objects."""

    id = serializers.UUIDField()
    name = serializers.CharField()
