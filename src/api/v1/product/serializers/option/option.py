import json

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .additional_serializers import ProductOptionSerializer
from ... import services
from ...models import ProductOption


class ProductOptionsListSerializer(serializers.Serializer):
    """Serializer that represent options that are connected to products."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    options = serializers.SerializerMethodField()

    @extend_schema_field(ProductOptionSerializer(many=True))
    def get_options(self, instance):
        """To convert from RawQuerySet. See services.option for details."""
        return json.loads(instance.options)


class ProductOptionInputSeriliazer(serializers.ModelSerializer):
    """Serializer for input data to add a new option."""

    name = serializers.CharField()
    parent_id = serializers.UUIDField(allow_null=True)

    def create(self, validated_data):
        """Create and return a new option with optional parameter parent_id."""
        parent_id = validated_data.pop("parent_id")
        if parent_id:
            return services.create_child_option(validated_data["name"], parent_id)
        else:
            return services.create_root_option(validated_data["name"])

    class Meta:  # noqa D106
        model = ProductOption
        fields = ["name", "parent_id"]
