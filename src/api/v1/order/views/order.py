from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter

from api.base.permissions import StaffPermission, OwnerPermission
from api.v1.order import services
from api.v1.order.filters import OrderFilter
from api.v1.order.serializers import OrderSerializer, OrderUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Handlers for operation with orders."""

    http_method_names = ["get", "post", "patch"]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created_at", "updated_at", "status"]
    ordering = ["-created_at"]

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action in {"list", "partial_update", "destroy"}:
            permission_classes = [StaffPermission]
        elif self.action == "retrieve":
            permission_classes = [OwnerPermission, StaffPermission]
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

    def create(self, request, *args, **kwargs):
        """## New order creation are able to any user even non-authenticated."""

    def destroy(self, request, *args, **kwargs):
        """## To perform this action user must be a staff."""
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """## To perform this action user must be a staff.

        ### Ordering are able for following fields. Specify them in ordering parameter:
            - status
            - created_at
            - updated_at
        ### Default ordering is by created date ascending. To change behavior just add:
            - To obtain ASCENDING ordering just provide field specified above.
            - To obtain DESCENDING add - to a field name.

        ### All other specified fields are utilized in filtering.
        """
        return super().list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """## To perform this action user must be a staff."""
        return super().partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """## Available for owner or for staff members."""
        return super().retrieve(request, *args, **kwargs)
