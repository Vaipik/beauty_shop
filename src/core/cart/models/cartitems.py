import decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base.models import Base
from core.cart.models import Cart
from core.product.constants import PRODUCT_PRICE_MAX_DIGITS


class CartItem(Base):
    """Describe item of cart."""

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        to="product.Product", on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Item quantity"), default=1)
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=PRODUCT_PRICE_MAX_DIGITS, decimal_places=2
    )

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart item"
        verbose_name_plural = "Cart items"

    def __str__(self) -> str:
        return f"{self.product}, price - {self.price}"

    @property
    def cost(self) -> decimal.Decimal:
        """Calculate the total cost of item in the cart."""
        return self.quantity * self.price
