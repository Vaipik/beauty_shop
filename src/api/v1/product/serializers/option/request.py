from rest_framework import serializers

from api.v1.product.models import ProductOption


class ProductOptionCreateRequestSeriliazer(serializers.ModelSerializer):
    """Serializer for input data to add a new option."""

    name = serializers.CharField()
    parent_id = serializers.UUIDField(allow_null=True, format="hex_verbose")

    # def create(self, validated_data):
    #     """Create and return a new option with optional parameter parent_id."""
    #     parent_id = validated_data.pop("parent_id")
    #     if parent_id:
    #         return services.create_child_option(validated_data["name"], parent_id)
    #     else:
    #         return services.create_root_option(validated_data["name"])

    class Meta:  # noqa D106
        model = ProductOption
        fields = ["id", "name", "parent_id"]
        read_only_fields = ["id"]
