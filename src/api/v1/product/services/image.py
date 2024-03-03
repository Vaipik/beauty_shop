from typing import Collection

from django.db.models import QuerySet

from core.product.models import ProductImage, ProductItem


def get_all_images_related_to_products() -> QuerySet[ProductImage]:
    """Return all images that are binded to products."""
    return ProductImage.objects.select_related("product").filter(product__isnull=False)


def get_all_images_not_related_to_products() -> QuerySet[ProductImage]:
    """Return all images that are not binded to products."""
    return ProductImage.objects.select_related("product").filter(product__isnull=True)


def update_product_item_images(images: Collection[dict], product: ProductItem) -> None:
    """Create images for given product."""
    for image in images:
        pk = image.pop("id")
        ProductImage.objects.filter(pk=pk).update(**image, product=product)
