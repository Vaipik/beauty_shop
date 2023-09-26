from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.v1.product.filters import ProductFilter
from api.v1.product.serializers import (
    ProductListResponseSerializer,
    ProductSerializer,
)
from api.v1.product import services


class ProductViewSet(viewsets.ModelViewSet):
    """Represent product routes. PUT method is excluded because of NULL."""

    http_method_names = ["get", "post", "patch", "delete"]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        """Different endpoints require different serializers."""
        if self.action == "list":
            return ProductListResponseSerializer
        if self.action in {"create", "retrieve", "partial_update"}:
            return ProductSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """Different serializers require different querysets."""
        if self.action == "list":
            return services.get_list_products()
        if self.action in ["retrieve", "destroy", "partial_update"]:
            return services.get_detail_product(self.kwargs["pk"])
        return super().get_queryset()

    @extend_schema(
        # override default docstring extraction
        description="Return a list of products."
        "Note that products have only one image - main image. This endpoint can be used"
        "for main page of website. Also endpoint has filters which are designed "
        "as query parameters and they are optional.",
    )
    def list(self, request):  # noqa D102
        # your non-standard behaviour
        return super().list(request)

    @extend_schema(
        description="Endpoint to create a new product. Please note that image ordering"
        " must starts with 1 and be consequent, otherwise you will be obtain"
        " an error."
    )
    def create(self, request, *args, **kwargs):  # noqa D102
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Endpoint that returns a detail information about product for user",
    )
    def retrieve(self, request, pk=None):  # noqa D102
        return super().retrieve(request, pk)

    @extend_schema(
        description="Endpoint to update a product. Please note that image ordering"
        " must starts with 1 and be consequent, otherwise you will be obtain"
        " an error."
    )
    def partial_update(self, request, *args, **kwargs):  # noqa D102
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete product and images."""
        instance = self.get_queryset()
        services.delete_product(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
