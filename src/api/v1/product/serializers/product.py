from rest_framework import serializers

from ..models import Product
from ..serializers.image import ProductImageSerializer


class ProductOutputListSerializer(serializers.ModelSerializer):
    """Specified for list display view.

    Primary usage is at the main page to obtain product list with only one image.
    """

    image = serializers.SerializerMethodField()

    class Meta:  # noqa D106
        model = Product
        fields = ["id", "name", "description", "status", "image"]
        read_only_fields = ["id"]

    def get_image(self, obj: Product) -> str | None:
        """Return image url with order equals to 1 or None if it does not exist."""
        return obj.img_url if obj.img_url else None


class ProductOutputDetailSerializer(serializers.ModelSerializer):
    """Detailed view of product with full list of images and options."""

    images = ProductImageSerializer(many=True, read_only=True)
    manufacturer = serializers.SlugRelatedField(slug_field="name", read_only=True)

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
