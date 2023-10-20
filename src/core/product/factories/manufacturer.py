import factory.fuzzy

from core.product.models import ProductManufacturer


class ProductManufacturerFactory(factory.django.DjangoModelFactory):
    """Manufacturers factory."""

    class Meta:
        model = ProductManufacturer
