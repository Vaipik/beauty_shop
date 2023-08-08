from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers import (
    ProductCategoryOutputListSerializer,
    ProductOutputListSerializer,
    ProductOptionsListSerializer,
)
from .. import services


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """Viewset for categories that are binded for products."""

    serializer_class = ProductCategoryOutputListSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        """Choose which queryset should be queried."""
        if self.action == "list":
            return services.get_categories_binded_to_products()
        if self.action == "products":
            return services.get_products_for_category(self.kwargs["pk"])
        if self.action == "options":
            return services.get_product_options_in_category(self.kwargs["pk"])
        return super().get_queryset()

    @extend_schema(
        responses=ProductOutputListSerializer(many=True),
        description="List of products for category.",
    )
    @action(detail=True, methods=["get"], serializer_class=ProductOutputListSerializer)
    def products(self, request, pk=None):
        """Extra route to obtain list of products for a category."""
        queryset = self.get_queryset()
        serialzer = self.get_serializer(queryset, many=True)
        return Response(serialzer.data, status=200)

    @extend_schema(
        responses=ProductOptionsListSerializer(many=True),
        description="List of product options that are presented in category.",
    )
    @action(detail=True, methods=["get"], serializer_class=ProductOptionsListSerializer)
    def options(self, request, pk=None):
        """Extra route to obtain list of products for a category."""
        queryset = self.get_queryset()
        serialzer = self.get_serializer(queryset, many=True)
        return Response(serialzer.data, status=200)
