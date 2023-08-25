from uuid import UUID

from django.db import transaction
from django.db.models import QuerySet
from django.db.models.query import RawQuerySet, Prefetch

from core.product.models import Product, ProductOption, ProductImage


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
        Product.objects.prefetch_related("images", "options")
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


@transaction.atomic
def create_product(validated_data: dict) -> Product:
    """Create a product instance with nested data in one transaction.

    Product instance using an existing categories, options and manufacturer to create
    but images are saving to db. Mean they were not previously loaded.
    """
    manufacturer = validated_data.pop("manufacturer")
    categories = validated_data.pop("categories")
    options = validated_data.pop("options")
    images = validated_data.pop("images")
    product = Product.objects.create(
        **validated_data,
        manufacturer=manufacturer,
    )
    for image in images:
        ProductImage.objects.create(
            img_order=image["img_order"], img_path=image["img_path"], product=product
        )
    product.categories.add(*categories)
    product.options.add(*options)

    return product


@transaction.atomic
def patch_product(validated_data: dict) -> Product:
    """Perform a data update for product in database."""
    id_ = validated_data.pop("id")
    product = (
        Product.objects.prefetch_related("images", "categories", "options")
        .select_related("manufacturer")
        .get(pk=id_)
    )
    manufacturer = validated_data.pop("manufacturer")
    categories = validated_data.pop("categories")
    options = validated_data.pop("options")
    images = validated_data.pop("images")
    new_images = filter(lambda x: x.get("id") is None, images)
    old_images = filter(lambda x: x.get("id") is not None, images)
    if categories:
        product.categories.clear()
        product.categories.add(*categories)
    if options:
        product.options.clear()
        product.options.add(*options)
    if manufacturer:
        product.manufacturer = manufacturer
    if images:
        if new_images:
            [
                ProductImage.objects.create(
                    img_order=image["img_order"],
                    img_path=image["img_path"],
                    product=product,
                )
                for image in new_images
            ]
        if old_images:
            [product.images.update(img_order=image["img_order"]) for image in images]
    product.save()
    return product


def delete_product(instance: Product) -> None:
    """Delete product from database with images."""
    instance.delete()
