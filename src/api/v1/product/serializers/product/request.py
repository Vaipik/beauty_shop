from rest_framework import serializers, status

from core.product.models import Product, ProductImage
from api.v1.product import services
from api.v1.product.serializers import ProductImageCreateRequestSerializer
from .common import ProductImagePatchSerializer


class ProductCreateRequestSerializer(serializers.ModelSerializer):
    """Serializer to create a new product with nested images, options and cats."""

    images = ProductImageCreateRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ["id"]

    def create(self, validated_data) -> Product:
        """To create a product instance with nested serializers."""
        request = self.context.get("request")
        images = request.FILES.getlist("images")
        if not images:
            raise serializers.ValidationError("You need to upload images.")
        return services.create_product(validated_data, images)


class ProductPatchRequestSerializer(serializers.ModelSerializer):
    """Serializer for updating product data."""

    images = ProductImagePatchSerializer(many=True)

    class Meta:
        model = Product
        exclude = ["id"]

    def validate_images(self, value: list[ProductImage]) -> list[ProductImage] | None:
        """Validate image ordering. It must be a sequence starting from 1."""
        if value:
            sorted_images = sorted(value, key=lambda x: x.img_order)
            for idx, image in enumerate(sorted_images, 1):
                if idx != image.img_order:
                    raise serializers.ValidationError(
                        detail="Ordering must be consistent",
                        code=status.HTTP_400_BAD_REQUEST,
                    )
            return value
