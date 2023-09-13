import decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base.models import Base
from core.product.constants import PRODUCT_PRICE_MAX_DIGITS


class OrderItem(Base):
    """Order item."""

    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=PRODUCT_PRICE_MAX_DIGITS,
        decimal_places=2,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name=_("Item quantity"),
        default=1,
    )
    order = models.ForeignKey(
        to="Order",
        on_delete=models.SET_NULL,
        related_name="items",
        null=True,
    )
    product = models.ForeignKey(
        to="product.Product",  # app_label.ModelName
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_items",
    )

    class Meta:
        db_table = "order_items"
        verbose_name = "Order item"
        verbose_name_plural = "Order items"

    def __str__(self) -> str:
        return f"{self.product} [{self.price=}, {self.quantity=}]"

    @property
    def cost(self) -> decimal.Decimal:
        """Total price for item according to its quantity."""
        return self.quantity * self.price
