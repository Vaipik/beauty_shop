from api.base.permissions import StaffPermission
from api.v1.order import services
from api.v1.order.filters import OrderFilter
from api.v1.order.serializers import OrderSerializer, OrderUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter


class OrderViewSet(viewsets.ModelViewSet):
    """Handlers for operation with orders.

    - To sort by creation or update date, use the "ordering" parameter in the URL.
      - Example: orders/?ordering=created_at - by increase
      - Example: orders/?ordering=-created_at - by decrease
    - To filter by status or user or date, use the next URL
      - Example: orders/?created_date=2024-01-17 - for a specific date
      - Example:
        /?created_range_after=2024-01-01&created_range_before=2024-01-17-the period
    - To paginate, use the 'page_size' parameter in the URL
      - Example: orders/?page_size=2
    """

    http_method_names = ["get", "post", "patch"]
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action == "partial_update":
            permission_classes = [StaffPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

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
