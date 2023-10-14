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

    def list(self, request):  # noqa D102
        """Provide an array with all products and their filters.

        Array will contain all products that have been marked as main card and
        have at least one image with ordering equals to 1. Other will be ignored.
        Siblings field returns an array of objects that are marked not as main card and
        have same logic for image.
        """
        return super().list(request)

    def create(self, request, *args, **kwargs):
        """Endpoint to create a new product.

        Note that image ordering must begin from 1 and be consequent. To add siblings
        you need to provide only their ids.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Provide a detailed data about product."""
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Perform an update for a product. It has same restrictions as POST."""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Pefrom hard-delet for product and images."""
        instance = self.get_queryset()
        services.delete_product(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
