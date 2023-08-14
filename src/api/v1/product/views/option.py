from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from ..serializers import ProductOptionsListSerializer, ProductOptionInputSeriliazer
from .. import services


class ProductOptionViewSet(viewsets.ModelViewSet):
    """Viewset for options that are binded for products."""

    serializer_class = ProductOptionsListSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        """Choose which queryset should be queried."""
        if self.action == "list":
            return services.get_options_binded_to_products()
        return super().get_queryset()

    def get_serializer_class(self):  # noqa D102
        if self.action == "list":
            return ProductOptionsListSerializer
        if self.action == "create":
            return ProductOptionInputSeriliazer
        return super().get_serializer_class()

    @extend_schema(
        request=ProductOptionInputSeriliazer, responses=ProductOptionsListSerializer
    )
    def create(self, request, *args, **kwargs):  # noqa D102
        return super().create(request, *args, **kwargs)
