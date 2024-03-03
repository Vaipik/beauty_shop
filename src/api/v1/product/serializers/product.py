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
    newPrice = ProductCurrencySerializer(many=True, source="price")
    oldPrice = ProductCurrencySerializer(many=True, source="price", read_only=True)

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
            "rating",
            "sku",
            "categories",
            "options",
            "images",
            "feedbacks",
            "createdAt",
            "updatedAt",
            "oldPrice",
            "newPrice",
        ]
        exclude_fields = ["created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer to create a new product with nested images, options and cats."""

    isLuxury = serializers.BooleanField(source="is_luxury")
    items = ProductItemSerializer(many=True, source="product_items")

    class Meta:
        model = Product
        exclude = ["is_luxury"]
        read_only_fields = ["id"]

    def create(self, validated_data) -> Product:
        """To create a product instance with nested serializers."""
        items = validated_data.pop("items")
        product = services.create_product(validated_data, items)
        return product

    def update(self, instance, validated_data) -> Product:
        """Update product."""
        items = validated_data.pop("items", None)
        return services.update_product(instance, validated_data, items)
