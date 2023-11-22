from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.v1.cart.serializers.cart import ShoppingCartSerializer
from core.product.models import Product
from core.cart.models.cart import ShoppingCart, CartItem


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Cart processing class for registered user."""

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        """Display data only for a specific user."""
        user = self.request.user
        if user.is_authenticated:
            queryset = ShoppingCart.objects.filter(user=user)
            return queryset
        else:
            return ShoppingCart.objects.none()

    def create(self, request, *args, **kwargs):
        """Cart creation method. Request POST."""
        user = request.user
        if user.is_authenticated:
            product_id = request.data.get("product")
            quantity = request.data.get("quantity")
        else:
            return Response(
                {"error": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not product_id or not quantity:
            return Response(
                {"error": "Product and quantity are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = get_object_or_404(Product, id=product_id)
        cart = self.create_or_update_cart(user, product, quantity)
        # return response
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_or_update_cart(self, user, product, quantity):
        """Check the existence of the user and the cart.."""
        cart, created = ShoppingCart.objects.get_or_create(user=user)
        self.add_product_to_cart(cart, product, quantity)
        return cart

    def add_product_to_cart(self, cart, product, quantity):
        """Сhange the number of items in the cart using POST, PUT, PATCH requests."""
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

    def update(self, request, *args, **kwargs):
        """Cart updation method. Request PUT, PATCH."""
        user = request.user
        cart_id = kwargs.get("pk")
        cart = get_object_or_404(ShoppingCart, id=cart_id, user=user)
        products = request.data.get("cartitem_set", [])
        self.update_cart(cart, products)

        # return response
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_cart(self, cart, products):
        """Receive an updated product and quantity."""
        for product_data in products:
            product_id = product_data.get("product")
            quantity = product_data.get("quantity")

            if not product_id or not quantity:
                return Response(
                    {"error": "Product and quantity are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product = get_object_or_404(Product, id=product_id)

            self.add_product_to_cart(cart, product, quantity)

    def destroy(self, request, *args, **kwargs):
        """Remove an item from the cart."""
        user = request.user
        cart_id = kwargs.get("pk")
        cart = get_object_or_404(ShoppingCart, id=cart_id, user=user)
        products = request.data.get("cartitem_set", [])
        self.delete_cart_item(cart, products)
        cart.refresh_from_db()  # refresh the data of the cart object from the database.
        serializer = self.get_serializer(cart)

        # return response
        # if cart is empty, delete cart
        if cart.cartitem_set.count() == 0:
            cart.delete()
            return Response(
                {"message": "ShoppingCart deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete_cart_item(self, cart, products):
        """Receive deleted product."""
        for product in products:
            product_id = product.get("product")
            cart_item = get_object_or_404(CartItem, cart=cart, product=product_id)
            cart_item.delete()
