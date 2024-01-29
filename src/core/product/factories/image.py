import factory.fuzzy
from factory import SubFactory

from core.product.factories.product import ProductFactory
from core.product.models import ProductImage


class ProductImageFactory(factory.django.DjangoModelFactory):
    """Factory for generating instances of the ProductImage model."""

    img_path = factory.django.ImageField()
    img_order = factory.fuzzy.FuzzyInteger(low=0, high=10)
    product = SubFactory(ProductFactory)

    class Meta:
        model = ProductImage
        django_get_or_create = ["img_path"]
