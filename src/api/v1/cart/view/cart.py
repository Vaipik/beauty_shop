from uuid import UUID

from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.v1.cart.serializers.cart import CartSerializer, CartItemSerializer
from core.cart.models.cart import Cart, CartItem


class CartViewSet(viewsets.ModelViewSet):
    """Handlers for operation with carts."""

    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get a queryset based on the action."""
        if self.action in {"retrieve", "partial_update", "destroy"}:
            return get_detail_cart(pk=self.kwargs["pk"])

    def create(self, request, *args, **kwargs):
        """Create the serializer with request data and user context."""
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete Cart."""
        instance = self.get_object()
        delete_cart(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_detail_cart(pk: UUID) -> QuerySet[Cart]:
    """Return detailed data for a specific cart."""
    return (
        Cart.objects.prefetch_related("items")
        .select_related("user")
        .filter(pk=pk, is_active=True)
    )


def delete_cart(cart):
    """Make the cart inactive when an order is created or there are no items."""
    cart.is_active = False
    cart.save()


def check_cart(cart):
    """Сheck cart for items."""
    if cart.items.count() == 0:
        delete_cart(cart)


class CartItemViewSet(viewsets.ModelViewSet):
    """Handlers for operation with items."""

    http_method_names = ["get", "delete"]
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get a queryset based on the action."""
        if self.action in {"retrieve", "destroy"}:
            return get_detail_cartitem(pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        """Delete CartItem."""
        instance = self.get_object()
        cart = instance.cart
        delete_cart_item(instance, cart)
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_detail_cartitem(pk: UUID) -> QuerySet[CartItem]:
    """Return detailed data for a specific item."""
    return CartItem.objects.select_related("cart", "product").filter(pk=pk)


def delete_cart_item(cartitem, cart):
    """Delete item."""
    cartitem.delete()
    check_cart(cart)
