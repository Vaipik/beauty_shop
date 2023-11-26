from factory import Sequence, post_generation
from factory.django import DjangoModelFactory
from core.product.models import ProductCategory


class ProductCategoryFactory(DjangoModelFactory):
    """Factory for product category."""

    name = Sequence(lambda n: f"Category_{n}")

    class Meta:
        model = ProductCategory
        django_get_or_create = ("name",)

    @post_generation
    def add_children(self, create, extracted, **kwargs):
        """Create child category."""
        if not create:
            return
        if extracted:
            for n in range(extracted):
                ProductCategoryFactory(parent=self)
