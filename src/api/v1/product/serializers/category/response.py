import json

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.product.models import ProductCategory
from .common import ProductCategorySerializer


class ProductCategoryCreateResponseSeriliazer(serializers.ModelSerializer):
    """Serializer to be used in reponse when category created."""

    class Meta:  # noqa D106
        model = ProductCategory
        fields = ["id", "name"]


class ProductCategoryListResponseSerializer(serializers.Serializer):
    """Serializer that represent categories that are binded to products."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    categories = serializers.SerializerMethodField()

    @extend_schema_field(ProductCategorySerializer(many=True))
    def get_categories(self, instance):
        """To convert from RawQuerySet. See services.category for details."""
        return json.loads(instance.categories)
