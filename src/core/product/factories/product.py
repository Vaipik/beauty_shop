import factory.fuzzy

from core.product import constants
from core.product.models import Product

from .manufacturer import ProductManufacturerFactory


class ProductFactory(factory.django.DjangoModelFactory):
    """Product factory."""

    name = factory.Sequence(lambda x: f"Product_{x}")
    description = factory.fuzzy.FuzzyText()
    rating = factory.fuzzy.FuzzyDecimal(
        low=0,
        high=5,
    )
    price = factory.fuzzy.FuzzyDecimal(
        low=0,
        high=int("9" * (constants.PRODUCT_PRICE_MAX_DIGITS - 2)),  # 9999999 without .XX
    )
    sku = factory.fuzzy.FuzzyInteger(low=0, high=2147483647)  # PositiveIntegerField
    status = factory.fuzzy.FuzzyChoice(Product.ProductStatusChoices.values)
    sibling_name = factory.fuzzy.FuzzyText(length=6)  # noqa
    main_card = False  # To override when instantiating just pass main_card=True
    is_luxury = True  # same as above
    manufacturer = factory.SubFactory(ProductManufacturerFactory)
    # categories = factory.SubFactory(...)
    # options = factory.SubFactory(...)

    class Meta:
        model = Product
        django_get_or_create = ["name"]
