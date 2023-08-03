from uuid import UUID

from django.db.models import F, QuerySet

from ..models import Product


def get_list_products() -> QuerySet[Product]:
    """Return queryset with prefetched images and with extra field for img_url."""
    return Product.objects.prefetch_related("images").annotate(
        img_url=F("images__img_path")
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
