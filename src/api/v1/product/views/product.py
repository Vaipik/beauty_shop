from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from api.v1.product.filters import ProductFilter
from api.v1.product.serializers import (
    ProductDetailResponseSerializer,
    ProductListResponseSerializer,
    ProductCreateRequestSerializer,
    ProductFullResponseSerializer,
)
from api.v1.product import services


class ProductViewSet(viewsets.ModelViewSet):
    """Represent product routes. PUT method is excluded because of NULL."""

    http_method_names = ["get", "post"]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        """Different endpoints require different serializers."""
        if self.action == "list":
            return ProductListResponseSerializer
        if self.action == "retrieve":
            return ProductDetailResponseSerializer
        if self.action == "create":
            return ProductCreateRequestSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """Different serializers require different querysets."""
        if self.action == "list" or "create":
            return services.get_list_products()
        if self.action == "retrieve":
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
        request=ProductCreateRequestSerializer,
        responses=ProductFullResponseSerializer,
    )
    def create(self, request, *args, **kwargs):  # noqa D102
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Endpoint that returns a detail information about product for user",
        responses=ProductDetailResponseSerializer,
    )
    def retrieve(self, request, pk=None):  # noqa D102
        return super().retrieve(request, pk)
