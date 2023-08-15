from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..serializers import (
    ProductOptionListResponseSerializer,
    ProductOptionCreateRequestSeriliazer,
    ProductOptionCreateResponseSeriliazer,
)
from .. import services


class ProductOptionViewSet(viewsets.ModelViewSet):
    """Viewset for options that are binded for products."""

    serializer_class = ProductOptionListResponseSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        """Choose which queryset should be queried."""
        if self.action == "list":
            return services.get_options_binded_to_products()
        return super().get_queryset()

    def get_serializer_class(self):  # noqa D102
        if self.action == "list":
            return ProductOptionListResponseSerializer
        if self.action == "create":
            return ProductOptionCreateRequestSeriliazer
        return super().get_serializer_class()

    @extend_schema(
        description="",
        request=ProductOptionCreateRequestSeriliazer,
        responses=ProductOptionCreateResponseSeriliazer,
    )
    def create(self, request, *args, **kwargs):  # noqa D102
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if parent_id := serializer.data.get("parent_id"):
            option = services.create_child_option(serializer.data["name"], parent_id)
        else:
            option = services.create_root_option(serializer.data["name"])

        response = ProductOptionCreateResponseSeriliazer(option)
        return Response(data=response.data, status=status.HTTP_201_CREATED)
