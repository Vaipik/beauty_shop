from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.v1.cart.serializers.cart import CartSerializer
from api.v1.cart.services.cart import get_detail_cart, delete_cart


class CartViewSet(viewsets.ModelViewSet):
    """Handlers for operation with carts."""

    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return the queryset for the view."""
        if self.action in {"retrieve", "partial_update", "destroy"}:
            return get_detail_cart(pk=self.kwargs["pk"])

    def create(self, request, *args, **kwargs):
        """Create a new cart."""
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a cart."""
        instance = self.get_object()
        delete_cart(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
