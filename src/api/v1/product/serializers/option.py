from rest_framework import serializers

from ..models import ProductCategoryOption


class ProductCategoryOptionSerializer(serializers.ModelSerializer):  # noqa D101
    class Meta:  # noqa D106
        model = ProductCategoryOption
        fields = "__all__"
