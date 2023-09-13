from core.product.models import Product
from core.order.models import Order, OrderItem


def create_order_items(order: Order, items: list[dict]) -> None:
    """Create order items for given order instance."""
    order_items = []
    for item in items:
        price = Product.objects.get(pk=item["product_id"]).price
        order_items.append(
            OrderItem(
                price=price,
                quantity=item["quantity"],
                order=order,
                product_id=item["product_id"],
            )
        )
    OrderItem.objects.bulk_create(order_items)
