from rest_framework import serializers

from core.product.models import ProductImage


class ProductImageListResponseSerializer(serializers.ModelSerializer):
    """Serializer for GET response."""

    order = serializers.IntegerField(source="img_order", allow_null=True)
    url = serializers.ImageField(source="img_path", use_url=True)

    class Meta:
        model = ProductImage
        fields = ["id", "order", "url"]


class ProductImageCreateResponseSerializer(serializers.ModelSerializer):
    """Serializer that used only for POST response image creation."""

    url = serializers.URLField(source="image")

    class Meta:
        model = ProductImage
        fields = ["id", "url"]
        read_only_fields = ["id"]
