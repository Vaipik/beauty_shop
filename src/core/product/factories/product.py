import factory.fuzzy
from factory import RelatedFactoryList, SubFactory

from core.product import constants
from core.product.factories.category import ProductCategoryFactory
from core.product.factories.manufacturer import ProductManufacturerFactory
from core.product.factories.option import ProductOptionFactory
from core.product.models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory for generating instances of the Product model."""

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
    status = factory.fuzzy.FuzzyChoice(Product.ProductStatusChoices.values)
    currency = factory.fuzzy.FuzzyChoice(Product.ProductCurrencyChoice.values)
    sibling_name = factory.fuzzy.FuzzyText(length=6)  # noqa
    main_card = False  # To override when instantiating just pass main_card=True
    is_luxury = True  # same as above
    manufacturer = SubFactory(ProductManufacturerFactory)  # ForeignKey
    categories = RelatedFactoryList(
        ProductCategoryFactory, factory_related_name="product_categories"
    )  # ManyToManyField
    options = RelatedFactoryList(
        ProductOptionFactory, factory_related_name="product_options"
    )
    siblings = RelatedFactoryList(
        "core.product.factories.ProductFactory", factory_related_name="product_sibling"
    )  # Circular imports

    class Meta:
        model = Product
        django_get_or_create = ["name"]
