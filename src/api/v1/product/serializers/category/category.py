import json

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .additional_serializers import ProductCategorySerializer


class ProductCategoryOutputListSerializer(serializers.Serializer):
    """Serializer that represent options that are connected to products."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    categories = serializers.SerializerMethodField()

    @extend_schema_field(ProductCategorySerializer(many=True))
    def get_categories(self, instance):
        """To convert from RawQuerySet. See services.category for details."""
        return json.loads(instance.categories)
