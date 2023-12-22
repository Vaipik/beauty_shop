import random

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from core.cart.tests.factories import (
    UserFactory,
    ProductFactory,
    CartFactory,
    CartItemFactory,
)

register(UserFactory)
register(ProductFactory)
register(CartFactory)
register(CartItemFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product(db, product_factory):
    return product_factory.create()


@pytest.fixture
def product1(db, product_factory):
    return product_factory.create()


@pytest.fixture
def user(db, user_factory):
    return user_factory.create()


@pytest.fixture
def auth(api_client, user):
    api_client.force_authenticate(user=user)


@pytest.fixture
def cart(db, user, cart_factory):
    return cart_factory.create(user=user)


@pytest.fixture
def cartitem(db, cart, product, cart_item_factory):
    return cart_item_factory.create(cart=cart, product=product, price=product.price)


@pytest.fixture
def cart_with_items(db, cart, product, product1, cart_item_factory):
    cart_item_factory.create(cart=cart, product=product, price=product.price)
    cart_item_factory.create(cart=cart, product=product1, price=product1.price)
    return cart


@pytest.fixture
def data_quantity(db, user, product):
    return {
        "user": user.id,
        "items": [{"productID": str(product.id), "quantity": random.randint(1, 100)}],
    }


@pytest.fixture
def data_prod(db, user, product1):
    return {"user": user.id, "items": [{"productID": str(product1.id)}]}
