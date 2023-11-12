from factory import SubFactory, Sequence, post_generation
from factory.django import DjangoModelFactory
from core.product.models import ProductCategory


class ProductCategoryFactory(DjangoModelFactory):
    """Factory for product category."""

    class Meta:
        model = ProductCategory

    name = Sequence(lambda n: f"Category_{n}")
    parent = SubFactory("self", null=True)

    @post_generation
    def add_children(self, create, extracted, **kwargs):
        """Create child category."""
        if not create:
            return
        if extracted:
            for n in range(extracted):
                ProductCategoryFactory(parent=self)
