from rest_framework import viewsets

from api.v1.product.serializers import ProductImageRequestSerializer
from core.product.models import ProductImage


class ProductImageViewSet(viewsets.ModelViewSet):
    """Endpoints for operations with images."""

    serializer_class = ProductImageRequestSerializer
    http_method_names = ["get", "post"]
    queryset = ProductImage.objects.all()
