from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, parsers, status
from rest_framework.response import Response

from api.v1.product.serializers import ProductImageCreateRequestSerializer
from api.v1.product.serializers.image import (
    ProductImageCreateResponseSerializer,
)
from core.product.models import ProductImage


class ProductImageViewSet(viewsets.ModelViewSet):
    """Endpoints for operations with images."""

    http_method_names = ["get", "post", "delete"]
    queryset = ProductImage.objects.all()
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    def get_serializer_class(self):  # noqa D102
        if self.action == "create":
            return ProductImageCreateRequestSerializer
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
