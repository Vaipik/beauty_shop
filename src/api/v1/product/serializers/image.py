from rest_framework import serializers

from ..models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):  # noqa D101
    img_url = serializers.ImageField(source="img_path", use_url=True)

    class Meta:  # noqa D106
        model = ProductImage
        fields = ["img_url", "img_order"]
