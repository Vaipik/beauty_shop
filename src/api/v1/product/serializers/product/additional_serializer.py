from rest_framework import serializers


class ProductOptionListSerializer(serializers.Serializer):
    """Serializer for `Option` objects."""

    name = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField())
