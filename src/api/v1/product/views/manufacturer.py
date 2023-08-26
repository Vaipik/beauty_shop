from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from core.product.models import ProductManufacturer

from ..serializers import (
    ProductManufacturerResponseSerializer,
    ProductManufacturerCreateRequestSerializer,
)


class ProductManufacturerViewSet(viewsets.ModelViewSet):
    """Viewset for ProductManufacturer."""

    serializer_class = ProductManufacturerResponseSerializer
    queryset = ProductManufacturer.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]

    @extend_schema(
        description="This endpoint is used to create manufacturer. If you want to "
        "create manufacturer without description you don't need to pass a description,"
        " leave it NULL. ",
        request=ProductManufacturerCreateRequestSerializer,
        responses=ProductManufacturerResponseSerializer,
    )
    def create(self, request, *args, **kwargs):
        """Create manufacturer."""
        return super().create(request, *args, **kwargs)
