import factory.fuzzy
from factory import SubFactory

from core.cart.factories.cart import CartFactory
from core.product.factories import ProductFactory
from core.cart.models import CartItem
from core.product import constants


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
