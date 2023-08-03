from rest_framework import viewsets

from ..serializers import ProductCategoryOutputSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """All categories."""

    serializer_class = ProductCategoryOutputSerializer

    http_method_names = ["get", "post", "patch", "delete"]
