from rest_framework import serializers

from core.product.models import ProductOption
from api.v1.product.serializers.common import TreeListResponseSerializer


class ProductOptionCreateResponseSeriliazer(serializers.ModelSerializer):
    """Serializer for created option."""

    class Meta:
        model = ProductOption
        fields = ["id", "name"]


class ProductOptionListResponseSerializer(TreeListResponseSerializer):
    """Serializer that represent existing options with their suboptions."""

    pass


class ProductOptionPatchResponseSerializer(TreeListResponseSerializer):
    """Serializer that represent updated options tree."""

    pass
