from rest_framework import viewsets

from ..serializers import ProductOptionsListSerializer
from .. import services


class ProductOptionViewSet(viewsets.ModelViewSet):
    """Viewset for options that are binded for products."""

    serializer_class = ProductOptionsListSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        """Choose which queryset should be queried."""
        if self.action == "list":
            return services.get_options_binded_to_products()
        return super().get_queryset()
