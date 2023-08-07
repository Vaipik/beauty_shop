from rest_framework import serializers

from ..models import Product
from ..serializers.image import ProductImageSerializer
from ..serializers.option import (
    ProductOptionsListSerializer,
)
from .. import services


class ProductOutputListSerializer(serializers.ModelSerializer):
    """Specified for list display view.

    Primary usage is at the main page to obtain product list with only one image.
    """

    img_url = serializers.SerializerMethodField()
    options = ProductOptionsListSerializer(many=True, read_only=True)

    class Meta:  # noqa D106
        model = Product
        fields = ["id", "name", "description", "status", "img_url", "options"]
        read_only_fields = ["id"]

    def get_img_url(self, obj: Product) -> str | None:
        """Return image url with order equals to 1 or None if it does not exist."""
        request = self.context.get("request")
        img_url = services.get_product_image_url(obj)
        return request.build_absolute_uri(img_url)


class ProductOutputDetailSerializer(serializers.ModelSerializer):
    """Detailed view of product with full list of images and options."""

    images = ProductImageSerializer(many=True, read_only=True)
    manufacturer = serializers.SlugRelatedField(slug_field="name", read_only=True)
    options = serializers.SerializerMethodField()

    class Meta:  # noqa D106
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "rating",
            "options",
            "images",
            "manufacturer",
        ]

    def get_options(self, instance: Product):
        """Return product options in nested format {parent: [child]}."""
        options = services.get_product_options(instance.pk)
        return [{"name": option.name, "options": option.options} for option in options]
