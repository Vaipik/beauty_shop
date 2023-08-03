from rest_framework import serializers

from ..models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):  # noqa D101
    class Meta:  # noqa D106
        model = ProductImage
        fields = ["img_path", "img_order"]

    def to_representation(self, instance: ProductImage):
        """To get url from FileField."""
        rep = super(ProductImageSerializer, self).to_representation(instance)
        rep["img_path"] = instance.img_path.url
        return rep
