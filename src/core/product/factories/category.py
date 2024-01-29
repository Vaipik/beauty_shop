import factory.fuzzy
from factory import RelatedFactoryList

from core.product.factories.option import ProductOptionFactory
from core.product.models import ProductCategory


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    """Factory for generating instances of the ProductCategory model."""

    name = factory.Sequence(lambda x: f"Product_{x}")
    options = RelatedFactoryList(
        ProductOptionFactory, factory_related_name="category_options"
    )

    class Meta:
        model = ProductCategory
