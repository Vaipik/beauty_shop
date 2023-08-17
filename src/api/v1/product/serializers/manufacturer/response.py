from rest_framework import serializers

from core.product.models import ProductManufacturer


class ProductManufacturerResponseSerializer(serializers.ModelSerializer):
    """Schema to create a manufacturer."""

    class Meta:  # noqa D106
        model = ProductManufacturer
        fields = ["id", "name"]
