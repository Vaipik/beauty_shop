from uuid import UUID

from django.db import transaction
from django.db.models import QuerySet

from core.order.models import Order

from .item import create_order_items


def get_orders_list() -> QuerySet[Order]:
    """Return a list with all orders."""
    return Order.objects.prefetch_related("items").select_related("user")


def get_detail_order(pk: UUID) -> QuerySet[Order]:
    """Return detailed data for product."""
    return Order.objects.prefetch_related("items").select_related("user").filter(pk=pk)


@transaction.atomic
def create_order(items: list[dict], validated_data: dict) -> Order:
    """Create new product and return its instance.

    This function is used to create an order with nested order items in one transaction.
    :param items: list of serialized order items data.
    :param validated_data: validated order data.
    """
    order = Order.objects.create(**validated_data)
    create_order_items(order, items)
    return order
