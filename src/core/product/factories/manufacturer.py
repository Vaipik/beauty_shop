import factory.fuzzy

from core.product.models import ProductManufacturer


class ProductManufacturerFactory(factory.django.DjangoModelFactory):
    """Factory for manufacturer."""

    name = factory.Sequence(lambda x: f"Manufacturer_{x}")
    description = factory.LazyAttribute(lambda x: f"{x.name} description")

    class Meta:
        model = ProductManufacturer
        django_get_or_create = ["name"]
