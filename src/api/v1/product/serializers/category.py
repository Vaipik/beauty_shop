from rest_framework import serializers

from core.product.models import ProductCategory


class ProductCategoryCreateResponseSeriliazer(serializers.ModelSerializer):
    """Serializer to be used in response when category created."""

    class Meta:
        model = ProductCategory
        fields = ["id", "name"]
