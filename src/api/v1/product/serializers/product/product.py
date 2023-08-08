from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.v1.product.models import Product
from api.v1.product.serializers.image import ProductImageSerializer
from api.v1.product import services
from .additional_serializer import ProductOptionListSerializer


class ProductOutputListSerializer(serializers.ModelSerializer):
    """Specified for list display view.

    Primary usage is at the main page to obtain product list with only one image.
    """

    img_url = serializers.SerializerMethodField()

    class Meta:  # noqa D106
        model = Product
        fields = ["id", "name", "manufacturer", "price", "rating", "sku", "img_url"]

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
        exclude = ["id", "categories"]

    @extend_schema_field(ProductOptionListSerializer)
    def get_options(self, instance: Product):
        """Return product options in nested format {parent: [child]}."""
        options = services.get_product_options(instance.pk)
        return [{"name": option.name, "options": option.options} for option in options]
