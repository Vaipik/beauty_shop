from rest_framework import viewsets

from api.v1.order.serializers import OrderCreateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Handlers for operation with orders."""

    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = OrderCreateSerializer
