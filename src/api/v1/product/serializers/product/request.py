from rest_framework import serializers

from core.product.models import Product
from api.v1.product import services
from api.v1.product.serializers import ProductImageCreateRequestSerializer


class ProductCreateRequestSerializer(serializers.ModelSerializer):
    """Serializer to create a new product with nested images, options and cats."""

    images = ProductImageCreateRequestSerializer(many=True)

    class Meta:
        model = Product
        exclude = ["id"]

    def create(self, validated_data) -> Product:
        """To create a product instance with nested serializers."""
        return services.create_product(validated_data)
