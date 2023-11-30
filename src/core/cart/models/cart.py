import decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    Sum,
    ExpressionWrapper,
    F,
    DecimalField,
    PositiveIntegerField,
    UniqueConstraint,
    Q,
)
from django.utils.translation import gettext_lazy as _

from core.base.models import Base, TimeStampedBase
from core.product.constants import PRODUCT_PRICE_MAX_DIGITS

User = get_user_model()


class Cart(Base, TimeStampedBase):
    """Describe cart."""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="carts")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        constraints = [
            UniqueConstraint(
                fields=["user", "is_active"],
                condition=Q(is_active=True),
                name="unique_active_cart_for_user",
            )
        ]

    @property
    def total_quantity(self):
        """Count the total number of items in the cart."""
        return self.items.aggregate(
            total_quantity=ExpressionWrapper(
                Sum("quantity"), output_field=PositiveIntegerField()
            )
        )["total_quantity"]

    @property
    def total_price(self):
        """Calculate the total cost of items in the cart."""
        return self.items.aggregate(
            total_price=ExpressionWrapper(
                Sum(F("quantity") * F("price"), output_field=DecimalField()),
                output_field=DecimalField(),
            )
        )["total_price"]


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
