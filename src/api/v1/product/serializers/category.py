import json

from rest_framework import serializers


class ProductCategoryListSerializer(serializers.Serializer):
    """Serializer that represent options that are connected to products."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    categories = serializers.SerializerMethodField()

    def get_categories(self, instance):
        """To convert from RawQuerySet. See services.category for details."""
        return json.loads(instance.categories)
