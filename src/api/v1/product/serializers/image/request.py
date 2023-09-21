from rest_framework import serializers

from core.product.models import ProductImage


class ProductImageCreateRequestSerializer(serializers.ModelSerializer):
    """Upload an image that is related to a product."""

    image = serializers.ImageField(source="img_path")

    class Meta:
        model = ProductImage
        fields = ["id", "image"]
        read_only_fields = ["id"]


class ProductImagePatchRequestSerializer(serializers.ModelSerializer):
    """Serializer used to update image ordering."""

    imgOrder = serializers.IntegerField(source="img_order")

    class Meta:
        model = ProductImage
        fields = ["id", "imgOrder"]
