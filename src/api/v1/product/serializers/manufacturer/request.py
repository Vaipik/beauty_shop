from rest_framework import serializers

from core.product.models import ProductManufacturer


class ProductManufacturerCreateRequestSerializer(serializers.ModelSerializer):
    """Schema to create a manufacturer."""

    class Meta:
        model = ProductManufacturer
        fields = ["name"]
