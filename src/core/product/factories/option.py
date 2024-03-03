import factory.fuzzy

from core.product.models import ProductOption


class ProductOptionFactory(factory.django.DjangoModelFactory):
    """Factory for generating instances of the ProductOption model."""

    name = factory.Sequence(lambda x: f"Product_{x}")

    class Meta:
        model = ProductOption
