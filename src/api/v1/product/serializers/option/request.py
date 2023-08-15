from rest_framework import serializers

from api.v1.product.models import ProductOption


class ProductOptionCreateRequestSeriliazer(serializers.ModelSerializer):
    """Serializer for input data to add a new option."""

    name = serializers.CharField()
    parent_id = serializers.UUIDField(allow_null=True, format="hex_verbose")

    class Meta:  # noqa D106
        model = ProductOption
        fields = ["id", "name", "parent_id"]
        read_only_fields = ["id"]
