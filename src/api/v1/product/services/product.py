from typing import Collection
from uuid import UUID

from django.db import transaction
from django.db.models import QuerySet
from django.db.models.query import Prefetch

from core.product.models import Product, ProductCurrency, ProductImage, ProductItem

from .image import update_product_item_images


def get_list_products() -> QuerySet[Product]:
    """Return products that marked as main and have img order equalst to 1.

    Note that if product have no images attached than this product will not be listed
    in queryset. Same is for siblings images.
    """
    # return _get_related_list_view(Product.objects.prefetch_related("product_items"))
    return Product.objects.prefetch_related("product_items").all()


def get_detail_product(pk: UUID) -> QuerySet[Product]:
    """Return queryset for given product primary key.

    Prefetching relations of images and options tables and doing joining manufacturer.

    :param pk: primary key of the desired product.
    :return: queryset with the only ony product.
    """
    return (
        Product.objects.prefetch_related("product_items")
        .select_related("manufacturer")
        .filter(pk=pk)
    )


def _get_related_list_view(obj: QuerySet[Product]) -> QuerySet[Product]:
    """Operate with related objects for list-views."""
    return obj.prefetch_related(
        Prefetch(
            lookup="images",
            queryset=ProductImage.objects.filter(img_order=1),
        ),
        Prefetch(
            lookup="siblings",
            queryset=(
                Product.objects.filter(
                    images__img_order=1, main_card=False
                ).prefetch_related(
                    Prefetch(
                        lookup="images",
                        queryset=ProductImage.objects.filter(img_order=1),
                    )
                )
            ),
        ),
    ).select_related("manufacturer")


def get_products_for_category(category_id: UUID) -> QuerySet[Product]:
    """Return all products for a category."""
    return _get_related_list_view(
        Product.objects.filter(main_card=True, categories__id=category_id)
    )


def get_products_by_manufacturer(pk: UUID):
    """Return a queryset with product instances related to given manufacturer."""
    return (
        Product.objects.prefetch_related(
            Prefetch("images", queryset=ProductImage.objects.filter(img_order=1)),
            "categories",
        )
        .select_related("manufacturer")
        .filter(manufacturer_id=pk)
    )


@transaction.atomic
def create_product(
    validated_data: dict,
    items: Collection[dict],
) -> Product:
    """Create a product instance with nested data in one transaction."""
    product = Product.objects.create(
        name=validated_data["name"],
        description=validated_data["description"],
        is_luxury=validated_data["is_luxury"],
        manufacturer_id=validated_data["manufacturer"],
    )
    create_product_items(product, items)
    return product


def create_product_items(product: Product, items: Collection[dict]) -> None:
    """Create using bulk create."""
    ProductItem.objects.bulk_create(
        [_create_product_item(product, item) for item in items]
    )


def _create_product_item(product: Product, item: dict) -> ProductItem:
    """For inner use only. Used in bulk_create to create a product and variants.

    :param product: existing product instance.
    :param item: product_item attrs.
    :return: ProductItem instance without calling save()
    """
    images = item.pop("images")
    options = item.pop("options")
    categories = item.pop("categories")
    prices: list[dict] = item.pop("price")

    product_item = ProductItem(**item, product=product)
    product_item.options.add(*options)
    product_item.categories.add(*categories)
    create_prices(product_item, prices)
    update_product_item_images(images, product_item)
    return product_item


def create_prices(product: ProductItem, prices: list[dict]) -> None:
    """Create prices for a product item instance."""
    ProductCurrency.objects.bulk_create(
        [
            ProductCurrency(
                product=product,
                currency_id=price["currency_id"],
                value=price["value"],
            )
            for price in prices
        ]
    )


@transaction.atomic
def update_product(
    product: Product,
    validated_data: dict,
    items: list[dict],
) -> Product:
    """Create a product instance with nested data in one transaction."""
    if validated_data:
        [setattr(product, attr, validated_data[attr]) for attr in validated_data]

    update_product_items(items)
    product.save()
    return product


def update_prices(product: ProductItem, prices: list[dict]) -> None:
    """Create prices for a product item instance."""
    for price in prices:
        currency = ProductCurrency.objects.filter(
            product=product, currency_id=price["currency_id"]
        )
        currency.value = price["value"]
        currency.save()


def update_product_items(items: list[dict]) -> None:
    """Update all product items."""
    [_update_product_item(item) for item in items]


def _update_product_item(item: dict):
    """For inner use only. Used in bulk_create to create a product and variants.

    :param item: product_item attrs.
    :return: ProductItem instance without calling save()
    """
    images = item.pop("images")
    options = item.pop("options")
    categories = item.pop("categories")
    prices: list[dict] = item.pop("price")
    product_item = ProductItem.objects.get(item["id"])
    [setattr(product_item, attr, item[attr]) for attr in item]
    product_item.options.add(*options)
    product_item.categories.add(*categories)
    update_prices(product_item, prices)
    product_item.images.update(img_order=None)
    for image in images:
        img_order = image["img_order"]
        product_item.images.filter(id=image["id"]).update(img_order=img_order)
    product_item.save()
    return product_item


def delete_product(instance: Product) -> None:
    """Delete product from database with images."""
    instance.delete()
