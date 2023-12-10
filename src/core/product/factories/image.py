import factory.fuzzy

from core.product.models import ProductImage

from .product import ProductFactory


class ProductImageFactory(factory.django.DjangoModelFactory):
    """Image factory."""

    img_path = factory.django.ImageField()
    img_order = factory.Iterator([i for i in range(1, 11)])
    product = factory.SubFactory(ProductFactory)

    class Meta:
        model = ProductImage
