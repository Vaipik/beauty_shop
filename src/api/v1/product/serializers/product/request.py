from rest_framework import serializers

from core.product.models import Product
from api.v1.product import services
from api.v1.product.serializers.image.request import ProductImagePatchRequestSerializer


class ProductSerializer(serializers.ModelSerializer):
    """Serializer to create a new product with nested images, options and cats."""

    images = ProductImagePatchRequestSerializer(many=True, read_only=False)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id"]

    def create(self, validated_data) -> Product:
        """To create a product instance with nested serializers."""
        images = validated_data.pop("images")
        return services.create_product(validated_data, images)

    def update(self, instance, validated_data):
        """Update product."""
        images = validated_data.pop("images")
        return services.update_product(instance, validated_data, images)

    def validate_images(self, images: dict) -> dict | None:
        """If user didn't upload new images performs a rearrange of existing images."""
        if not images:
            raise serializers.ValidationError("You need to upload images.")

        for idx, image in enumerate(sorted(images, key=lambda x: x["img_order"]), 1):
            if idx != image["img_order"]:
                raise serializers.ValidationError("Image ordering must be consequent")

        return images
