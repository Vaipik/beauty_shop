import factory.fuzzy

from core.product.models import ProductImage


class ProductImageFactory(factory.django.DjangoModelFactory):
    """Images factory."""

    class Meta:
        model = ProductImage
