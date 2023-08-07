import json

from rest_framework import serializers


class ProductOptionsListSerializer(serializers.Serializer):
    """Serializer that represent options that are connected to products."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    options = serializers.SerializerMethodField()

    def get_options(self, instance):
        """To convert from RawQuerySet. See services.option for details."""
        return json.loads(instance.options)
