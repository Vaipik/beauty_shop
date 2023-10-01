from typing import Collection
from uuid import UUID

from django.db import transaction
from django.db.models import QuerySet
from django.db.models.query import RawQuerySet, Prefetch

from core.product.models import Product, ProductOption, ProductImage
from .image import update_product_images


def get_list_products() -> QuerySet[Product]:
    """Return queryset with prefetched images and with extra field for img_url.

    Note that if product have no images attached to it such product will not be listed
    in queryset
    """
    return Product.objects.prefetch_related(
        Prefetch("images", queryset=ProductImage.objects.filter(img_order=1)),
        "categories",
    ).select_related("manufacturer")


def get_detail_product(pk: UUID) -> QuerySet[Product]:
    """Return queryset for given product primary key.

    Prefetching relations of images and options tables and doing joining manufacturer.

    :param pk: primary key of the desired product.
    :return: queryset with the only ony product.
    """
    return (
        Product.objects.prefetch_related("images", "options", "siblings", "categories")
        .select_related("manufacturer")
        .filter(pk=pk)
    )


def get_product_image_url(product: Product) -> str | None:
    """Accept object instance with filtered queryset via img_order equals to 1."""
    image = product.images.all()
    if image:
        return image[0].img_path.url


def get_product_options(product_id: UUID) -> RawQuerySet:
    """To have product options in combined view. Note: For single use only.

    :param product_id: primary key of desired product
    :return: RawQuerySet with parent.pk, parent.name and array of child.
    """
    query = """
        SELECT parent.id, parent.name, array_agg(child.name) as options
        FROM product_options AS parent
        LEFT JOIN product_options AS child
        ON child.path SIMILAR TO CONCAT(parent.path, '____')
        INNER JOIN product_options_m2m as m2m ON
        child.id = m2m.productoption_id
        WHERE m2m.product_id = %s
        GROUP BY parent.id, parent.name
    """

    raw_queryset = ProductOption.objects.raw(query, (product_id,))
    return raw_queryset


def get_products_for_category(category_id: UUID) -> QuerySet[Product]:
    """Return all products for a category."""
    return Product.objects.filter(categories__id=category_id)


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


def get_product_siblings(product: Product) -> Collection[dict]:
    """Query to obtain only id and values to display them in siblings field."""
    siblings = product.siblings.values("id", "name")
    return siblings


def add_siblings(product: Product, siblings: Collection[dict]) -> None:
    """Add siblings to related product and vice versa.

    Example:
    -------
        product_id and siblings ids are id_1, id_2. Code will make following pairs:
        product_id - id_1,
        product_id - id_2,
        id_1 - product_id,
        id_2 - product_id
    """
    ids = [sibling["id"] for sibling in siblings]
    for id_ in ids:
        sibling = Product.objects.get(pk=id_)
        product.siblings.add(id_)
        sibling.siblings.add(product.id)


def update_siblings(product: Product, siblings: Collection[dict]) -> None:
    """Perform an update of product siblings.

    First of all, delete all siblings and their pairs which are not present
    in the siblings collection.
    After deletion, add new siblings using add_siblings function.
    """
    ids = {sibling["id"] for sibling in siblings}
    siblings_to_remove = product.siblings.exclude(id__in=ids)
    for sibling in siblings_to_remove:
        product.siblings.remove(sibling)
        sibling.siblings.remove(product)
    add_siblings(product, siblings)


@transaction.atomic
def create_product(
    validated_data: dict, images: Collection[dict], siblings: Collection[dict]
) -> Product:
    """Create a product instance with nested data in one transaction.

    Product instance using an existing categories, options and manufacturer to create
    but images are saving to db. Mean they were not previously loaded.
    """
    categories = validated_data.pop("categories")
    options = validated_data.pop("options")
    product = Product.objects.create(
        **validated_data,
    )
    add_siblings(product, siblings)
    update_product_images(images, product)
    product.categories.add(*categories)
    product.options.add(*options)

    return product


@transaction.atomic
def update_product(
    product: Product,
    validated_data: dict,
    images: Collection[dict],
    siblings: Collection[dict],
) -> Product:
    """Perform a data update for product in database.

    :param product: instance that should be updated.
    :param validated_data: validated data obtained from serializer.
    :param images: images with ordering and ids.
    :param siblings: product siblings that must be updated.
    :return:
    """
    manufacturer = validated_data.pop("manufacturer")
    categories = validated_data.pop("categories")
    options = validated_data.pop("options")

    if categories:
        product.categories.add(*categories)
    if options:
        product.options.add(*options)
    if manufacturer:
        product.manufacturer = manufacturer
    if siblings:
        update_siblings(product, siblings)

    product.images.update(img_order=None)
    for image in images:
        img_order = image["img_order"]
        product.images.filter(id=image["id"]).update(img_order=img_order)

    return product


def delete_product(instance: Product) -> None:
    """Delete product from database with images."""
    instance.delete()
