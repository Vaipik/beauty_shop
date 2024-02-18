from rest_framework import serializers

from api.base.serializers import TimeStampedSerializer
from api.v1.feedback.serializers import FeedbackProductSerializer
from api.v1.product import services
from api.v1.product.serializers import ProductCurrencySerializer, ProductImageSerializer
from core.product.models import Product, ProductItem


class ProductItemSerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Exact product item."""

    feedbacks = FeedbackProductSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=False, allow_null=True)
    price = ProductCurrencySerializer(many=True)

    # @extend_schema_field(ProductOptionListSerializer(many=True))
    # def get_options(self, instance: Product):
    #     """Return product options in nested format {parent: [child]}."""
    #     options = services.get_product_options(instance.pk)
    #     return [{"name": option.name, "options": option.options} for option in options

    class Meta:
        model = ProductItem
        fields = [
            "id",
            "description",
            "name",
            "price",
            "rating",
            "sku",
            "categories",
            "options",
            "images",
            "feedbacks",
            "createdAt",
            "updatedAt",
        ]
        exclude_fields = ["created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer to create a new product with nested images, options and cats."""

    isLuxury = serializers.BooleanField(source="is_luxury")
    items = ProductItemSerializer(many=True)

    class Meta:
        model = Product
        exclude = ["is_luxury"]
        read_only_fields = ["id"]

    def create(self, validated_data) -> Product:
        """To create a product instance with nested serializers."""
        images = validated_data.pop("images")
        siblings = validated_data.pop("siblings")
        price = validated_data.pop("price")
        return services.create_product(validated_data, images, siblings, price)

    def update(self, instance, validated_data) -> Product:
        """Update product."""
        images = validated_data.pop("images", None)
        siblings = validated_data.pop("siblings", None)
        price = validated_data.pop("price", None)
        return services.update_product(
            instance, validated_data, images, siblings, price
        )

    def validate_images(self, images: dict) -> dict | None:
        """If user didn't upload new images performs a rearrange of existing images."""
        if not images:
            raise serializers.ValidationError("You need to upload images.")

        for idx, image in enumerate(sorted(images, key=lambda x: x["img_order"]), 1):
            if idx != image["img_order"]:
                raise serializers.ValidationError("Image ordering must be consequent")

        return images


class ProductListResponseSerializer(serializers.ModelSerializer):
    """Specified for list display view.

    Primary usage is at the main page to obtain product list with only one image.
    """

    items = ProductItemSerializer(many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "items"]
