import json

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .additional_serializers import ProductOptionSerializer


class ProductOptionsListSerializer(serializers.Serializer):
    """Serializer that represent options that are connected to products."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    options = serializers.SerializerMethodField()

    @extend_schema_field(ProductOptionSerializer(many=True))
    def get_options(self, instance):
        """To convert from RawQuerySet. See services.option for details."""
        return json.loads(instance.options)
