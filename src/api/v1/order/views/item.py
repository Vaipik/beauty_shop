from rest_framework import viewsets

from api.v1.order import services
from api.v1.order.serializers import OrderItemUpdateOrCreateSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """Order item endpoints."""

    http_method_names = ["post", "patch", "delete"]

    def get_queryset(self):  # noqa D102
        if self.action == "partial_update":
            return services.get_order_item(self.kwargs["pk"])
        return super().get_queryset()

    def get_serializer_class(self):  # noqa D102
        if self.action in {"partial_update", "create"}:
            return OrderItemUpdateOrCreateSerializer
