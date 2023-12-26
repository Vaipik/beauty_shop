from django.urls import reverse
from rest_framework import status

from api.v1.cart.serializers import CartSerializer
from core.order.models import Order


def test_create_cart(api_client, auth, user, data_prod):
    """Check the creation of a new Cart and CartItem instance."""

    url = reverse("cart:carts-list")
    response = api_client.post(url, data_prod, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert user.carts.filter(is_active=True).count() == 1


def test_create_or_update_cart(api_client, auth, user, cart, cartitem, data_prod):
    """Add item to existing cart."""

    url = reverse("cart:carts-list")
    response = api_client.post(url, data_prod, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert cart.items.count() == 2


def test_update_cart_product(api_client, auth, user, cart, cartitem, data_quantity):
    """Check the update of the quantity of item in the cart."""

    quantity = data_quantity["items"][0]["quantity"]
    url = reverse("cart:carts-detail", args=[cart.id])
    response = api_client.patch(url, data_quantity, format="json")
    cartitem.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert cartitem.quantity == quantity


def test_update_cart_nonexistent_product(api_client, auth, user, cart, data_quantity):
    """Check to update a nonexistent item in the cart."""

    url = reverse("cart:carts-detail", args=[cart.id])
    response = api_client.patch(url, data_quantity, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        f"Product with id {data_quantity['items'][0]['productID']} does not exist in the cart."
        == response.data[0]
    )


def test_destroy_cart(api_client, auth, user, cart_with_items):
    """Make the cart inactive."""

    url = reverse("cart:carts-detail", args=[cart_with_items.id])
    response = api_client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.carts.filter(is_active=True).count() == 0


def test_destroy_cartitem(api_client, auth, user, cart_with_items):
    """Remove item from cart."""

    url = reverse("cart:cart_items-detail", args=[cart_with_items.items.first().id])
    response = api_client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert cart_with_items.items.count() == 1


def test_destroy_cart_empty(api_client, auth, user, cart, cartitem):
    """Make the cart inactive if there are no items left in it."""

    url = reverse("cart:cart_items-detail", args=[cartitem.id])
    response = api_client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.carts.filter(is_active=True).count() == 0


def test_cart_deserialization(api_client, auth, user, data_prod):
    """Test data deserialization to create a new Cart."""

    serializer = CartSerializer(data=data_prod, context={"user": user})
    assert serializer.is_valid()
    cart = serializer.save()
    assert cart.user == user
    assert cart.is_active
    assert cart.items.count() == 1


def test_update_cart_prices_signal(cart, cartitem, product):
    """Check that the prices in the cart are updated when the product price changes."""

    old_price = product.price
    product.price = 50.0
    product.save()
    cartitem.refresh_from_db()

    assert cartitem.price == product.price
    assert cartitem.price != old_price


def test_delete_cart_after_order(api_client, auth, cart, user):
    """Check that the cart becomes inactive after creating an order."""

    Order.objects.create(user=user)
    cart.refresh_from_db()
    assert not cart.is_active
    assert user.carts.filter(is_active=True).count() == 0
