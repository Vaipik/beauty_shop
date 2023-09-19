from rest_framework import viewsets

from api.v1.order import services
from api.v1.order.serializers import OrderSerializer, OrderUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Handlers for operation with orders."""

    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = OrderSerializer

    def get_queryset(self):  # noqa D102
        if self.action == "list":
            return services.get_orders_list()
        if self.action in {"retrieve", "partial_update", "destroy"}:
            return services.get_detail_order(pk=self.kwargs["pk"])

    def get_serializer_class(self):  # noqa D102
        if self.action in {"list", "retrieve", "create"}:
            return OrderSerializer
        if self.action == "partial_update":
            return OrderUpdateSerializer
        return super().get_serializer_class()
