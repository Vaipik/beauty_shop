from uuid import UUID

from django.db.models import QuerySet

from core.order.models import Order


def get_orders_list() -> QuerySet[Order]:
    """Return a list with all orders."""
    return Order.objects.prefetch_related("items").select_related("user")


def get_detail_order(pk: UUID) -> QuerySet[Order]:
    """Return detailed data for product."""
    return Order.objects.prefetch_related("items").select_related("user").filter(pk=pk)


def create_order() -> Order:
    """Create new product and return its instance."""
    pass
