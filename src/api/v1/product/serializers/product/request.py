from rest_framework import serializers

from core.product.models import Product
from api.v1.product import services
from api.v1.product.serializers.image.request import ProductImagePatchRequestSerializer


class ProductCreateRequestSerializer(serializers.ModelSerializer):
    """Serializer to create a new product with nested images, options and cats."""

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

    oldImages = ProductImagePatchRequestSerializer(many=True, source="images")

    class Meta:
        model = Product
        exclude = ["id"]

    def update(self, instance, validated_data) -> Product:
        """Update images using json data of existing images and save new via form."""
        request = self.context.get("request")
        old_images = validated_data["images"]
        new_images = request.FILES.getlist("images")
        if not new_images:
            self.validate_old_images(old_images)
        updated_product = services.patch_product(instance, validated_data, new_images)
        return updated_product

    def validate_old_images(self, old_images: dict) -> None:
        """If user didn't upload new images performs a rearrange of existing images."""
        for idx, image in enumerate(
            sorted(old_images, key=lambda x: x["img_order"]), 1
        ):
            if idx != image["img_order"]:
                raise serializers.ValidationError("Image ordering must be consequent")
