from rest_framework import serializers

from core.product.models import ProductManufacturer


class ProductManufacturerSerializer(serializers.ModelSerializer):
    """Schema to operate with manufacturer."""

    class Meta:
        model = ProductManufacturer
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]
