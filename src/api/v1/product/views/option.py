from rest_framework import viewsets

from ..serializers import ProductCategoryOptionSerializer


class ProductCategoryOptionViewSet(viewsets.ModelViewSet):
    """All options for category."""

    serializer_class = ProductCategoryOptionSerializer

    http_method_names = ["get", "post", "patch", "delete"]
