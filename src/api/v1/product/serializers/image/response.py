from rest_framework import serializers

from core.product.models import ProductImage


class ProductImageListResponseSerializer(serializers.ModelSerializer):  # noqa D101
    img_path = serializers.ImageField(use_url=True)

    class Meta:  # noqa D106
        model = ProductImage
        fields = ["img_path", "img_order"]
