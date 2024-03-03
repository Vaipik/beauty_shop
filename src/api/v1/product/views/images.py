from drf_spectacular.utils import extend_schema
from rest_framework import parsers, permissions, status, viewsets
from rest_framework.response import Response

from api.base.permissions import StaffPermission
from api.v1.product.serializers import (
    ProductImageCreateRequestSerializer,
    ProductImageCreateResponseSerializer,
    ProductImageListSerializer,
)
from core.product.models import ProductImage


class ProductImageViewSet(viewsets.ModelViewSet):
    """Endpoints for operations with images."""

    http_method_names = ["get", "post", "delete"]
    queryset = ProductImage.objects.all()
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action in {"create", "partial_update", "destroy"}:
            permission_classes = [StaffPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):  # noqa D102
        if self.action == "create":
            return ProductImageCreateRequestSerializer
        if self.action in {"retrieve", "list"}:
            return ProductImageListSerializer
        return super().get_serializer_class()

    @extend_schema(
        operation_id="upload_file",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {"image": {"type": "string", "format": "binary"}},
            }
        },
        responses=ProductImageCreateResponseSerializer,
    )
    def create(self, request, *args, **kwargs):  # noqa D102
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = ProductImageCreateResponseSerializer(serializer.data)
        return Response(response.data, status=status.HTTP_201_CREATED, headers=headers)
