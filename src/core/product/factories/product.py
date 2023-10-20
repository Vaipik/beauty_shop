import factory.fuzzy

from core.product import constants
from core.product.models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    """Product factory that should be used only in tests."""

    class Meta:
        model = Product

    name = factory.fuzzy.FuzzyText()
    rating = factory.fuzzy.FuzzyDecimal(low=0, high=5)
    price = factory.fuzzy.FuzzyDecimal(
        low=0, high=constants.PRODUCT_PRICE_MAX_DIGITS - 2  # exclude after dot
    )
    sku = factory.fuzzy.FuzzyInteger(low=0, high=2147483647)  # PositiveInteger
