from rest_framework import serializers

from core.product.models import ProductManufacturer


class ProductManufacturerResponseSerializer(serializers.ModelSerializer):
    """Schema to create a manufacturer."""

    class Meta:
        model = ProductManufacturer
        fields = ["id", "name"]
