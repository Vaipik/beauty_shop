from uuid import UUID

from core.product.models import Product
from core.order.models import Order, OrderItem


def get_order_item(pk: UUID) -> str:
    """Get queryset with single order item."""
    return OrderItem.objects.select_related("order", "product").filter(pk=pk)


def create_order_item(order: Order, product_id: UUID, quantity: int) -> OrderItem:
    """Create a single order item for existing order."""
    price = Product.objects.get(pk=product_id).price
    order_item = OrderItem(
        price=price,
        quantity=quantity,
        order=order,
        product_id=product_id,
    )
    return order_item


def create_order_items(order: Order, items: list[dict]) -> None:
    """Create order items for given order instance."""
    OrderItem.objects.bulk_create(
        [
            create_order_item(
                order, product_id=item["product_id"], quantity=item["quantity"]
            )
            for item in items
        ]
    )
