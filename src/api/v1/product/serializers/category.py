from rest_framework import serializers

from ..models import ProductCategory


class ProductCategoryOutputSerializer(serializers.ModelSerializer):  # noqa D101
    class Meta:  # noqa D106
        model = ProductCategory
        fields = "__all__"
        read_only_fields = ["id"]
