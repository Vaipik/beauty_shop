import pytest
from api.v1.cart.serializers import CartSerializer
from core.cart.models import Cart, CartItem
from core.order.models import Order
from core.product.models import Product
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


def api_client():
    """Fixture to provide an instance  APIClient."""
    return APIClient()


@pytest.fixture
def user():
    """Fixture to create a test user."""
    return User.objects.create_user(username="Test User", password="Test Password")


@pytest.fixture
def product1():
    """Fixture to create a test product."""
    return Product.objects.create(
        name="Test Product 1", price=10.0, sku=1, main_card=True
    )


@pytest.fixture
def product2():
    """Fixture to create another test product."""
    return Product.objects.create(
        name="Test Product 2", price=30.0, sku=2, main_card=True
    )


@pytest.fixture
def cart(user):
    """Fixture to create a test cart."""
    return Cart.objects.create(user=user)


@pytest.fixture
def cartitem(user, cart, product1):
    """Fixture to create a test cartitem."""
    return CartItem.objects.create(cart=cart, product=product1, price=product1.price)


@pytest.mark.django_db
def test_create_cart(api_client, user, product1):
    """Check the creation of a new Cart and CartItem instance."""
    api_client.force_authenticate(user=user)
    data = {"user": user.id, "items": [{"productID": str(product1.id)}]}
    url = reverse("cart:carts-list")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Cart.objects.count() == 1
    assert CartItem.objects.count() == 1
    cart = Cart.objects.get()
    cartitem = CartItem.objects.get()
    assert cartitem.cart == cart
    assert cart.user == user


@pytest.mark.django_db
def test_create_or_update_cart(api_client, user, cart, cartitem, product2):
    """Add item to existing cart."""
    api_client.force_authenticate(user=user)
    data = {"user": user.id, "items": [{"productID": str(product2.id)}]}
    url = reverse("cart:carts-list")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert cart.items.count() == 2


@pytest.mark.django_db
def test_create_or_add_cart_item(api_client, user, cart, cartitem, product1):
    """Check the update of the quantity of item in the cart using the post method."""
    api_client.force_authenticate(user=user)
    data = {"user": user.id, "items": [{"productID": str(product1.id)}]}
    url = reverse("cart:carts-list")
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert cart.items.count() == 1
    assert cart.items.get().quantity == 2


@pytest.mark.django_db
def test_update_cart_product(api_client, user, cart, cartitem, product1):
    """Check the update of the quantity of an existing item in the cart."""
    api_client.force_authenticate(user=user)
    data = {"user": user.id, "items": [{"productID": str(product1.id), "quantity": 9}]}
    url = reverse("cart:carts-detail", args=[cart.id])
    response = api_client.patch(url, data, format="json")
    cartitem.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert cartitem.quantity == 9


@pytest.mark.django_db
def test_update_cart_nonexistent_product(api_client, user, cart, product1):
    """Check to update a nonexistent item in the cart."""
    api_client.force_authenticate(user=user)
    data = {"user": user.id, "items": [{"productID": str(product1.id), "quantity": 5}]}
    url = reverse("cart:carts-detail", args=[cart.id])
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert f"Product with id {product1.id} does not exist in the cart.", response.data[
        0
    ]


@pytest.mark.django_db
def test_destroy_cart(api_client, user, cart, cartitem):
    """Make the cart inactive."""
    api_client.force_authenticate(user=user)
    url = reverse("cart:carts-detail", args=[cart.id])
    response = api_client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.carts.filter(is_active=True).count() == 0


@pytest.mark.django_db
def test_destroy_cartitem(api_client, user, cart, cartitem):
    """Remove item from cart."""
    api_client.force_authenticate(user=user)
    url = reverse("cart:cart_items-detail", args=[cartitem.id])
    response = api_client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert cart.items.count() == 0


@pytest.mark.django_db
def test_destroy_cart_empty(api_client, user, cart, cartitem):
    """Make the cart inactive if there are no items left in it."""
    api_client.force_authenticate(user=user)
    url = reverse("cart:cart_items-detail", args=[cartitem.id])
    response = api_client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.carts.filter(is_active=True).count() == 0


@pytest.mark.django_db
def test_cart_deserialization(api_client, user, product1):
    """Test data deserialization to create a new Cart."""
    api_client.force_authenticate(user=user)
    data = {"user": user.id, "items": [{"productID": str(product1.id)}]}
    serializer = CartSerializer(data=data, context={"user": user})
    assert serializer.is_valid()
    cart = serializer.save()
    assert isinstance(cart, Cart)
    assert cart.user == user
    assert cart.is_active
    assert cart.items.count() == 1
    assert cart.items.get().product == product1


@pytest.mark.django_db
def test_update_cart_prices_signal(cart, cartitem, product1):
    """Check that the prices in the cart are updated when the product price changes."""
    old_price = product1.price
    product1.price = 50.0
    product1.save()
    cartitem.refresh_from_db()
    assert cartitem.price == product1.price
    assert cartitem.price != old_price


@pytest.mark.django_db
def test_delete_cart_after_order(api_client, cart, user):
    """Check that the cart becomes inactive after creating an order."""
    api_client.force_authenticate(user=user)
    Order.objects.create(user=user)
    cart.refresh_from_db()
    assert not cart.is_active
    assert user.carts.filter(is_active=True).count() == 0
