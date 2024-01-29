import factory.fuzzy

from core.product.models import ProductManufacturer


class ProductManufacturerFactory(factory.django.DjangoModelFactory):
    """Factory for generating instances of the ProductManufacturer model."""

    name = factory.Sequence(lambda x: f"Product_{x}")
    description = factory.fuzzy.FuzzyText()

    class Meta:
        model = ProductManufacturer
        django_get_or_create = ["name"]
