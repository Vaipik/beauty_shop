from uuid import UUID

from django.db.models import F, QuerySet
from django.db.models.query import RawQuerySet

from ..models import Product, ProductOption


def get_list_products() -> QuerySet[Product]:
    """Return queryset with prefetched images and with extra field for img_url.

    Note that if product have no images attached to it such product will not be listed
    in queryset
    """
    return (
        Product.objects.prefetch_related("images", "options")
        .filter(images__img_order=1)
        .annotate(img_path=F("images__img_path"))
    )


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


def get_product_image_url(product: Product) -> str:
    """Accept object instance with filtered queryset via img_order equals to 1."""
    return product.images.first().img_path.url


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
