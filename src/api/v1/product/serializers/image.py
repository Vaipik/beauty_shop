from rest_framework import serializers

from core.product.models import ProductImage


class ProductImageCreateRequestSerializer(serializers.ModelSerializer):
    """Upload an image via POST form using multipart/form-data."""

    image = serializers.ImageField(source="img_path")

    class Meta:
        model = ProductImage
        fields = ["id", "image"]
        read_only_fields = ["id"]


class ProductImageCreateResponseSerializer(serializers.ModelSerializer):
    """Serializer that used only for POST response image creation."""

    url = serializers.URLField(source="image")

    class Meta:
        model = ProductImage
        fields = ["id", "url"]
        read_only_fields = ["id"]


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer used to update image ordering."""

    id = serializers.UUIDField()
    order = serializers.IntegerField(source="img_order")
    url = serializers.ImageField(source="img_path", use_url=True, read_only=True)

    class Meta:
        model = ProductImage
        fields = ["id", "order", "url"]


class ProductImageListSerializer(ProductImageSerializer):
    """Serializer that extend base serializer and add productId field."""

    productId = serializers.UUIDField(
        source="product_id",
        format="hex_verbose",
        read_only=True,
    )

    class Meta(ProductImageSerializer.Meta):
        fields = ProductImageSerializer.Meta.fields + ["productId"]
