from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.base.serializers import TimeStampedSerializer
from api.v1.product import services
from api.v1.product.serializers.image import ProductImageSerializer
from api.v1.product.serializers.common import ProductOptionListSerializer
from api.v1.product.serializers.manufacturer import ProductManufacturerSerializer
from core.product.models import Product


class ProductSiblingsSerializer(serializers.Serializer):
    """Used to connect products with m2m to themselves."""

    id = serializers.UUIDField()
    name = serializers.CharField(read_only=True)


class ProductSerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Serializer to create a new product with nested images, options and cats."""

    images = ProductImageSerializer(many=True, read_only=False, allow_null=True)
    isLuxury = serializers.BooleanField(source="is_luxury")
    siblings = ProductSiblingsSerializer(many=True)

    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "is_luxury"]
        read_only_fields = ["id"]

    def create(self, validated_data) -> Product:
        """To create a product instance with nested serializers."""
        images = validated_data.pop("images")
        siblings = validated_data.pop("siblings")
        return services.create_product(validated_data, images, siblings)

    def update(self, instance, validated_data) -> Product:
        """Update product."""
        images = validated_data.pop("images")
        siblings = validated_data.pop("siblings")
        return services.update_product(instance, validated_data, images, siblings)

    def validate_images(self, images: dict) -> dict | None:
        """If user didn't upload new images performs a rearrange of existing images."""
        if not images:
            raise serializers.ValidationError("You need to upload images.")

        for idx, image in enumerate(sorted(images, key=lambda x: x["img_order"]), 1):
            if idx != image["img_order"]:
                raise serializers.ValidationError("Image ordering must be consequent")

        return images


class ProductDetailResponseSerializer(serializers.ModelSerializer):
    """Detailed view of product with full list of images and options."""

    images = ProductImageSerializer(many=True, read_only=True)
    manufacturer = ProductManufacturerSerializer()
    options = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ["id", "categories", "created_at", "updated_at"]

    @extend_schema_field(ProductOptionListSerializer(many=True))
    def get_options(self, instance: Product):
        """Return product options in nested format {parent: [child]}."""
        options = services.get_product_options(instance.pk)
        return [{"name": option.name, "options": option.options} for option in options]


class ProductListResponseSerializer(serializers.ModelSerializer):
    """Specified for list display view.

    Primary usage is at the main page to obtain product list with only one image.
    """

    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "rating", "sku", "images"]
