from rest_framework import serializers

from core.product.models import ProductImage


class ProductImageCreateRequestSerializer(serializers.ModelSerializer):
    """Upload an image that is related to a product."""

    class Meta:  # noqa D106
        model = ProductImage
        exclude = ["id"]
