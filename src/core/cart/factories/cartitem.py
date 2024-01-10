import factory.fuzzy
from factory import SubFactory

from core.cart.factories.cart import CartFactory

# from core.product.factories import ProductFactory
from core.cart.models import CartItem
from core.product import constants, models


# TODO: REMOVE IT!!!!
class ProductFactory(factory.django.DjangoModelFactory):
    """Stub."""

    name = factory.Sequence(lambda x: f"Product_{x}")
    description = factory.fuzzy.FuzzyText()
    rating = factory.fuzzy.FuzzyDecimal(
        low=0,
        high=5,
    )
    price = factory.fuzzy.FuzzyDecimal(
        low=0,
        high=int("9" * (constants.PRODUCT_PRICE_MAX_DIGITS - 2)),
        # 9999999 without .XX
    )
    sku = factory.fuzzy.FuzzyInteger(low=0, high=2147483647)  # PositiveIntegerField
    status = factory.fuzzy.FuzzyChoice(models.Product.ProductStatusChoices.values)
    sibling_name = factory.fuzzy.FuzzyText(length=6)  # noqa
    main_card = False  # To override when instantiating just pass main_card=True
    is_luxury = True  # same as above

    class Meta:
        model = models.Product
        django_get_or_create = ["name"]


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
