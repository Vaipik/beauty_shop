from rest_framework import serializers

from core.product.models import ProductOption


class ProductOptionCreateRequestSeriliazer(serializers.ModelSerializer):
    """Serializer for input data to add a new option."""

    name = serializers.CharField()
    parent_id = serializers.UUIDField(allow_null=True, format="hex_verbose")

    class Meta:
        model = ProductOption
        fields = ["id", "name", "parent_id"]
        read_only_fields = ["id"]
