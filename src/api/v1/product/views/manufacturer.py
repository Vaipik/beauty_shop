from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.product.models import ProductManufacturer

from api.v1.product import services
from api.v1.product.serializers import (
    ProductManufacturerSerializer,
    ProductListResponseSerializer,
)


class ProductManufacturerViewSet(viewsets.ModelViewSet):
    """Viewset for ProductManufacturer."""

    serializer_class = ProductManufacturerSerializer
    queryset = ProductManufacturer.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):  # noqa D102
        if self.action == "products":
            return services.get_products_by_manufacturer(self.kwargs["pk"])
        return super().get_queryset()

    @extend_schema(
        description="This endpoint is used to create manufacturer. If you want to "
        "create manufacturer without description you don't need to pass a description,"
        " leave it NULL. ",
    )
    def create(self, request, *args, **kwargs):
        """Create manufacturer."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses=ProductListResponseSerializer(many=True),
        description="Manufacturer products.",
    )
    @action(
        detail=True,
        methods=["get"],
        serializer_class=ProductListResponseSerializer,
    )
    def products(self, request, pk: UUID = None):
        """Extra route to obtain list of products related to manufacturer.."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
