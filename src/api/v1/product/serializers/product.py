from rest_framework import serializers

from ..models import Product
from ..serializers.image import ProductImageSerializer


class ProductOutputListSerializer(serializers.ModelSerializer):
    """Specified for list display view.

    Primary usage is at the main page to obtain product list with only one image.
    """

    img_url = serializers.SerializerMethodField()

    class Meta:  # noqa D106
        model = Product
        fields = ["id", "name", "description", "status", "img_url"]
        read_only_fields = ["id"]

    def get_img_url(self, obj: Product) -> str | None:
        """Return image url with order equals to 1 or None if it does not exist."""
        request = self.context.get("request")
        # print
        return request.build_absolute_uri("11")


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
