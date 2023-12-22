import factory.fuzzy
from django.contrib.auth import get_user_model
from factory import SubFactory

from core.cart.models import CartItem, Cart
from core.product import constants
from core.product.models import Product


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")


class ProductFactory(factory.django.DjangoModelFactory):
    """Product factory."""

    name = factory.Sequence(lambda x: f"Product_{x}")
    price = factory.fuzzy.FuzzyDecimal(
        low=0,
        high=int("9" * (constants.PRODUCT_PRICE_MAX_DIGITS - 2)),  # 999999 without .XX
    )
    sku = factory.fuzzy.FuzzyInteger(low=0, high=2147483647)  # PositiveIntegerField
    main_card = False  # To override when instantiating just pass main_card=True

    class Meta:
        model = Product


class CartFactory(factory.django.DjangoModelFactory):
    """Cart factory."""

    class Meta:
        model = Cart

    user = SubFactory(UserFactory)
    is_active = True


class CartItemFactory(factory.django.DjangoModelFactory):
    """CatrItem factory."""

    class Meta:
        model = CartItem

    cart = SubFactory(CartFactory)
    product = SubFactory(ProductFactory)
    quantity = factory.fuzzy.FuzzyInteger(low=0, high=100)
    price = factory.fuzzy.FuzzyDecimal(
        low=0,
        high=int("9" * (constants.PRODUCT_PRICE_MAX_DIGITS - 2)),  # 999999 without .XX
    )
