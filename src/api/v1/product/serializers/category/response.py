from rest_framework import serializers

from core.product.models import ProductCategory
from api.v1.product.serializers.common import TreeListResponseSerializer


class ProductCategoryCreateResponseSeriliazer(serializers.ModelSerializer):
    """Serializer to be used in reponse when category created."""

    class Meta:
        model = ProductCategory
        fields = ["id", "name"]


class ProductCategoryListResponseSerializer(TreeListResponseSerializer):
    """Serializer that represent existing categories with their subcategories."""

    pass
