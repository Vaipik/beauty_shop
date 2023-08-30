from rest_framework import serializers

from core.product.models import ProductImage


class ProductImageListResponseSerializer(serializers.ModelSerializer):
    """Serializer for GET response."""

    imgOrder = serializers.IntegerField(source="img_order")
    imgURL = serializers.ImageField(source="img_path", use_url=True)

    class Meta:
        model = ProductImage
        fields = ["id", "imgURL", "imgOrder"]
