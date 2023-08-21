from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.product.models import Product
from api.v1.product.serializers.image import ProductImageListResponseSerializer
from api.v1.product.serializers.manufacturer import (
    ProductManufacturerResponseSerializer,
)
from api.v1.product import services
from .common import ProductOptionListSerializer


class ProductListResponseSerializer(serializers.ModelSerializer):
    """Specified for list display view.

    Primary usage is at the main page to obtain product list with only one image.
    """

    # img_url = ProductImageListResponseSerializer(source="images", many=True)
    img_url = serializers.SerializerMethodField()
    manufacturer = ProductManufacturerResponseSerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "manufacturer", "price", "rating", "sku", "img_url"]

    def get_img_url(self, obj: Product) -> str | None:
        """Return image url with order equals to 1 or None if it does not exist."""
        request = self.context.get("request")
        img_url = services.get_product_image_url(obj)
        if img_url:
            return request.build_absolute_uri(img_url)


class ProductDetailResponseSerializer(serializers.ModelSerializer):
    """Detailed view of product with full list of images and options."""

    images = ProductImageListResponseSerializer(many=True, read_only=True)
    manufacturer = ProductManufacturerResponseSerializer()
    options = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["id", "categories", "created_at", "updated_at"]

    @extend_schema_field(ProductOptionListSerializer(many=True))
    def get_options(self, instance: Product):
        """Return product options in nested format {parent: [child]}."""
        options = services.get_product_options(instance.pk)
        return [{"name": option.name, "options": option.options} for option in options]


class ProductFullResponseSerializer(serializers.ModelSerializer):
    """Serializer using in admin panel to obtain full information about product."""

    images = ProductImageListResponseSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"
