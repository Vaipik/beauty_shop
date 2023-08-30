from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.v1.product.filters import ProductFilter
from api.v1.product.serializers import (
    ProductDetailResponseSerializer,
    ProductListResponseSerializer,
    ProductCreateRequestSerializer,
    ProductFullResponseSerializer,
    ProductPatchRequestSerializer,
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
        if self.action == "retrieve":
            return ProductDetailResponseSerializer
        if self.action == "create":
            return ProductCreateRequestSerializer
        if self.action == "partial_update":
            return ProductPatchRequestSerializer
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

    @extend_schema(
        description="Perform an update for product. If you want to add new images"
        "than leave id field empty or null.",
        request=ProductPatchRequestSerializer,
        responses=ProductDetailResponseSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        """PATCH for the product."""
        instance = self.get_queryset().all()[0]  # noqa only this works with filters
        request_serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        request_serializer.is_valid(raise_exception=True)
        updated_product = request_serializer.save()
        response_serializer = ProductDetailResponseSerializer(updated_product)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete product and images."""
        instance = self.get_queryset()
        services.delete_product(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
