from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.v1.cart.serializers import CartSerializer
from core.cart.models import Cart, CartItem
from core.order.models import Order
from core.product.models import Product

User = get_user_model()


class CartAPITestCase(APITestCase):
    """Test the cart application."""

    def setUp(self):
        """Create the necessary data for testing."""
        self.user = User.objects.create_user(
            username="Test User", password="Test Password"
        )
        self.client.force_authenticate(user=self.user)
        self.product1 = Product.objects.create(
            name="Test Product1", price=10.0, sku=1, main_card=True
        )
        self.product2 = Product.objects.create(
            name="Test Product2", price=20.0, sku=2, main_card=True
        )

    def test_create_cart(self):
        """Check the creation of a new Cart and CartItem instance."""
        data = {"user": self.user.id, "items": [{"productID": str(self.product1.id)}]}
        url = reverse("cart:carts-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 1)
        cart = Cart.objects.get()
        cartitem = CartItem.objects.get()
        self.assertEqual(cartitem.cart, cart)
        self.assertEqual(Cart.objects.get().user, self.user)

    def test_create_or_update_cart(self):
        """Add item to existing cart."""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart, product=self.product2, price=self.product2.price
        )
        data = {
            "user": self.user.id,
            "items": [
                {"productID": str(self.product1.id)},
            ],
        }
        url = reverse("cart:carts-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(cart.items.count(), 2)

    def test_create_or_add_cart_item(self):
        """Check the update cart.

        Check the update of the quantity of an existing item in the cart using
        the post method.
        """
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart, product=self.product2, price=self.product2.price
        )
        data = {"user": self.user.id, "items": [{"productID": str(self.product2.id)}]}
        url = reverse("cart:carts-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.get().quantity, 2)

    def test_update_cart_product(self):
        """Check the update of the quantity of an existing item in the cart."""
        cart = Cart.objects.create(user=self.user)
        cartitem = CartItem.objects.create(
            cart=cart, product=self.product2, price=self.product2.price
        )

        data = {
            "user": self.user.id,
            "items": [{"productID": str(self.product2.id), "quantity": 9}],
        }

        url = reverse("cart:carts-detail", args=[cart.id])
        response = self.client.patch(url, data, format="json")
        cartitem.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cartitem.quantity, 9)

    def test_update_cart_nonexistent_product(self):
        """Check the update of the quantity of a nonexistent item in the cart."""
        cart = Cart.objects.create(user=self.user)

        data = {
            "user": self.user.id,
            "items": [
                {"productID": str(self.product1.id), "quantity": 5},
            ],
        }

        url = reverse("cart:carts-detail", args=[cart.id])
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            f"Product with id {self.product1.id} does not exist in the cart.",
            response.data[0],
        )

    def test_destroy_cart(self):
        """Make the cart inactive."""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart, product=self.product2, price=self.product2.price
        )

        url = reverse("cart:carts-detail", args=[cart.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.filter(user=self.user, is_active=True).count(), 0)

    def test_destroy_cartitem(self):
        """Remove item from cart."""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart, product=self.product2, price=self.product2.price
        )
        cartitem2 = CartItem.objects.create(
            cart=cart, product=self.product1, price=self.product1.price
        )

        url = reverse("cart:cart_items-detail", args=[cartitem2.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(cart.items.count(), 1)

    def test_destroy_cart_empty(self):
        """Make the cart inactive if there are no items left in it."""
        cart = Cart.objects.create(user=self.user)
        cartitem1 = CartItem.objects.create(
            cart=cart, product=self.product2, price=self.product2.price
        )

        url = reverse("cart:cart_items-detail", args=[cartitem1.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cart.objects.filter(user=self.user, is_active=True).count(), 0)

    def test_cart_deserialization(self):
        """Test data deserialization to create a new Cart."""
        data = {"user": self.user.id, "items": [{"productID": str(self.product1.id)}]}

        serializer = CartSerializer(data=data, context={"user": self.user})
        self.assertTrue(serializer.is_valid())
        cart = serializer.save()
        self.assertIsInstance(cart, Cart)
        self.assertEqual(cart.user, self.user)
        self.assertTrue(cart.is_active)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product1)

    def test_update_cart_prices_signal(self):
        """Check update price.

        Check that the prices in the cart are updated when the product price changes.
        """
        cart = Cart.objects.create(user=self.user)
        cartitem = CartItem.objects.create(
            cart=cart, product=self.product1, price=self.product1.price
        )
        self.product1.price = 50.0
        self.product1.save()
        self.assertEqual(
            CartItem.objects.get(pk=cartitem.pk).price, self.product1.price
        )

    def test_delete_cart_after_order(self):
        """Check that the cart becomes inactive after creating an order."""
        Cart.objects.create(user=self.user)
        Order.objects.create(user=self.user)
        self.assertEqual(Cart.objects.filter(user=self.user, is_active=True).count(), 0)
