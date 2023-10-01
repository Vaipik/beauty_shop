from rest_framework import serializers


class ProductCategorySerializer(serializers.Serializer):
    """Serializer for `Option` objects."""

    id = serializers.UUIDField()
    name = serializers.CharField()


class ProductOptionListSerializer(serializers.Serializer):
    """Serializer for `Option` objects."""

    name = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField())


class TreeListResponseSerializer(serializers.Serializer):
    """Serializer that represent materialized path tree."""

    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=True)
    children = serializers.SerializerMethodField()

    def get_children(self, instance):
        """Parse children recursively."""
        children = instance.get_children()
        serializer = self.__class__(children, many=True)
        return serializer.data


class TreeCreateUpdateSerializer(serializers.Serializer):
    """Serializer used create or update MP models."""

    name = serializers.CharField(allow_null=True, allow_blank=True)
    parentId = serializers.UUIDField(allow_null=True, format="hex_verbose")
    toRoot = serializers.BooleanField(allow_null=False, default=False)
