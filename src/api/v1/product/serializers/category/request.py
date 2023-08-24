from rest_framework import serializers

from core.product.models import ProductCategory


class ProductCategoryCreateRequestSeriliazer(serializers.ModelSerializer):
    """Serializer for input data to add a new option."""

    parent_id = serializers.UUIDField(allow_null=True, format="hex_verbose")

    class Meta:
        model = ProductCategory
        fields = ["name", "parent_id"]


class ProductCategoryPartialUpdateRequestSerializer(serializers.Serializer):
    """Serializer used to perform a partial update of category."""

    name = serializers.CharField(allow_null=True, allow_blank=True)
    parent_id = serializers.UUIDField(allow_null=True, format="hex_verbose")
