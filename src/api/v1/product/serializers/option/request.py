from rest_framework import serializers

from core.product.models import ProductOption


class ProductOptionCreateRequestSeriliazer(serializers.ModelSerializer):
    """Serializer for input data to add a new option."""

    name = serializers.CharField()
    parentId = serializers.UUIDField(allow_null=True, format="hex_verbose")

    class Meta:
        model = ProductOption
        fields = ["id", "name", "parentId"]
        read_only_fields = ["id"]


class ProductOptionPartialUpdateRequestSerializer(serializers.Serializer):
    """Serializer used to perform a partial update of option."""

    name = serializers.CharField(allow_null=True, allow_blank=True)
    parentId = serializers.UUIDField(allow_null=True, format="hex_verbose")
