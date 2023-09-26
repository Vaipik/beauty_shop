from rest_framework import serializers

from core.product.models import ProductOption


class ProductOptionCreateResponseSeriliazer(serializers.ModelSerializer):
    """Serializer for created option."""

    class Meta:
        model = ProductOption
        fields = ["id", "name"]
