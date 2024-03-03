from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from api.v1.cart.serializers.cartitem import CartItemSerializer
from api.v1.cart.services.cartitem import delete_cart_item, get_detail_cartitem
from core.cart.models import CartItem


class CartItemViewSet(viewsets.ModelViewSet):
    """Handlers for operation with items."""

    http_method_names = ["get", "delete"]
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return the queryset for the view."""
        if getattr(self, "swagger_fake_view", False):  # drf-yasg comp
            return CartItem.objects.none()
        if self.action in {"retrieve", "destroy"}:
            return get_detail_cartitem(pk=self.kwargs["pk"])
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        """Delete a cartitem."""
        instance = self.get_object()
        cart = instance.cart
        delete_cart_item(instance, cart)
        return Response(status=status.HTTP_204_NO_CONTENT)
