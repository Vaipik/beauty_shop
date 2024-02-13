from rest_framework import permissions, viewsets

from api.base.permissions import StaffPermission
from api.v1.product.serializers.currency import (
    CurrencySerializer,
    ProductCurrencySerializer,
)
from core.product.models.currency import Currency, ProductCurrency


class ProductCurrencyViewSet(viewsets.ModelViewSet):
    """ViewSet provides CRUD operations for ProductCurrency instances.

    It handles GET, POST, PATCH, and DELETE requests for ProductCurrency objects.
    """

    http_method_names = ["get", "post", "patch", "delete"]
    queryset = ProductCurrency.objects.all()
    serializer_class = ProductCurrencySerializer

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action in {"create", "partial_update", "destroy"}:
            permission_classes = [StaffPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class CurrencyViewSet(viewsets.ModelViewSet):
    """ViewSet provides CRUD operations for Currency instances.

    It handles GET, POST, PATCH, and DELETE requests for Currency objects.
    """

    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action in {"create", "partial_update", "destroy"}:
            permission_classes = [StaffPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
