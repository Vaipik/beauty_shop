from typing import Collection

from django.db.models import QuerySet

from core.product.models import Product, ProductImage


def get_all_images_related_to_products() -> QuerySet[ProductImage]:
    """Return all images that are binded to products."""
    return ProductImage.objects.select_related("product").filter(product__isnull=False)


def get_all_images_not_related_to_products() -> QuerySet[ProductImage]:
    """Return all images that are not binded to products."""
    return ProductImage.objects.select_related("product").filter(product__isnull=True)


def create_images(images: Collection, product: Product) -> None:
    """Create images for given product."""
    images = [
        ProductImage(img_order=idx, img_path=image, product=product)
        for idx, image in enumerate(images, 1)
    ]
    ProductImage.objects.bulk_create(images)


def create_images_with_existing_images(
    images: Collection,
    product: Product,
    existing_order: list[int],
) -> None:
    """Create images with rearranged old images ordering."""
    missing_order = [
        idx for idx in range(max(existing_order)) if idx not in existing_order
    ]
    images = [
        ProductImage(img_order=idx, img_path=image, product=product)
        for idx, image in zip(missing_order, images)
    ]
    ProductImage.objects.bulk_create(images)