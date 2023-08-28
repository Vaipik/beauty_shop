from rest_framework import serializers


class ProductOptionListSerializer(serializers.Serializer):
    """Serializer for `Option` objects."""

    name = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField())


class ProductImagePatchSerializer(serializers.Serializer):
    """Serializer to patch. ID is optional."""

    id = serializers.UUIDField(allow_null=True)
    img_order = serializers.IntegerField()
    img_path = serializers.ImageField()
