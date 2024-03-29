from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from api.base.permissions import StaffPermission
from api.v1.product import services
from api.v1.product.filters import ProductFilter
from api.v1.product.serializers import ProductSerializer
from core.product.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    """Represent product routes. PUT method is excluded because of NULL."""

    http_method_names = ["get", "post", "patch", "delete"]
    filterset_class = ProductFilter
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action in {"create", "partial_update", "destroy"}:
            permission_classes = [StaffPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):  # noqa D102
        """Provide an array with all products and their filters.

        Array will contain all products that have been marked as main card and
        have at least one image with ordering equals to 1. Other will be ignored.
        Siblings field returns an array of objects that are marked not as main card and
        have same logic for image.
        """
        return super().list(request, *args, **kwargs)

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
