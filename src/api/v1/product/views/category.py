from rest_framework import viewsets

from ..serializers import ProductCategoryOutputListSerializer
from .. import services


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """Viewset for categories that are binded for products."""

    serializer_class = ProductCategoryOutputListSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        """Choose which queryset should be queried."""
        if self.action == "list":
            return services.get_categories_binded_to_products()
        return super().get_queryset()
