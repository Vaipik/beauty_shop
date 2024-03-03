from rest_framework import viewsets

from api.base.permissions import StaffPermission
from api.v1.product.serializers.currency import CurrencySerializer
from core.product.models import Currency


class CurrencyViewSet(viewsets.ModelViewSet):
    """ViewSet provides CRUD operations for Currency instances.

    It handles GET, POST, PATCH, and DELETE requests for Currency objects.
    """

    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Currency.objects.all()
    permission_classes = [StaffPermission]
    serializer_class = CurrencySerializer

    def create(self, request, *args, **kwargs):
        """Create new currency. Note that abbreviation is unqiue."""
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete currency data."""
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """Provide data about existing currencies."""
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Perform an update for given currency."""
        return super().partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Detail info about currency."""
        return super().retrieve(request, *args, **kwargs)
