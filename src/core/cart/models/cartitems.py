import decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base.models import Base
from core.product import constants as product_constants


class CartItem(Base):
    """Describe item of cart."""

    cart = models.ForeignKey(to="Cart", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        to="product.ProductItem", on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Item quantity"), default=1)
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=product_constants.PRODUCT_PRICE_MAX_DIGITS,
        decimal_places=2,
    )
    currency = models.CharField(
        verbose_name=_("Currency"),
        max_length=product_constants.CURRENCY_ABBREVIATION_MAX_LENGTH,
        default="UAH",
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
