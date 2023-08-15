from rest_framework import serializers

from api.v1.product.models import ProductImage


class ProductImageListResponseSerializer(serializers.ModelSerializer):  # noqa D101
    img_url = serializers.ImageField(source="img_path", use_url=True)

    class Meta:  # noqa D106
        model = ProductImage
        fields = ["img_url", "img_order"]
