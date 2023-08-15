import json

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from core.product.models import ProductOption
from .common import ProductOptionSerializer


class ProductOptionCreateResponseSeriliazer(serializers.ModelSerializer):
    """Serializer for created option."""

    class Meta:  # noqa D106
        model = ProductOption
        fields = ["id", "name"]


class ProductOptionListResponseSerializer(serializers.Serializer):
    """Serializer that represent options that are connected to products."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    options = serializers.SerializerMethodField()

    @extend_schema_field(ProductOptionSerializer(many=True))
    def get_options(self, instance):
        """To convert from RawQuerySet. See services.option for details."""
        return json.loads(instance.options)
