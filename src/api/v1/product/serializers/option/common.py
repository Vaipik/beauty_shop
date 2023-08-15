from rest_framework import serializers


class ProductOptionSerializer(serializers.Serializer):
    """Serializer for product list objects."""

    id = serializers.UUIDField()
    name = serializers.CharField()
