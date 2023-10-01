import json

from rest_framework import serializers

from core.product.models import ProductOption


class ProductOptionCreateResponseSeriliazer(serializers.ModelSerializer):
    """Serializer for created option."""

    class Meta:
        model = ProductOption
        fields = ["id", "name"]


class ProductOptionBindedSerializer(ProductOptionCreateResponseSeriliazer):
    """Serializer that are used to present binded options in a category."""

    children = serializers.SerializerMethodField()

    class Meta(ProductOptionCreateResponseSeriliazer.Meta):
        fields = ["id", "name", "children"]

    def get_children(self, obj):
        """Return parsed children as dictionary."""
        children_json = getattr(obj, "children", "[]")
        children_data = json.loads(children_json)
        return ProductOptionCreateResponseSeriliazer(children_data, many=True).data
