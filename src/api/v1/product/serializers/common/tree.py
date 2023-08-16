from rest_framework import serializers


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
