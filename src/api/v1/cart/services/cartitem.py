from uuid import UUID

from django.db.models import QuerySet

from api.v1.cart.services.cart import check_cart
from core.cart.models import CartItem


def get_detail_cartitem(pk: UUID) -> QuerySet[CartItem]:
    """Return detailed data for a specific item."""
    return CartItem.objects.select_related("cart", "product").filter(pk=pk)


def delete_cart_item(cartitem, cart):
    """Delete item."""
    cartitem.delete()
    check_cart(cart)
