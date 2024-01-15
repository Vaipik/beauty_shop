from core.order.models import Order


def check_product_in_order(product_id, user_id) -> bool:
    """Check if user has ordered product and order in success state."""
    return Order.objects.filter(
        status=Order.OrderStatus.SUCCESS, user_id=user_id, items__product__id=product_id
    ).exists()
