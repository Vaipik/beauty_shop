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

from core.base.models import Base, TimeStampedBase

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
        return self.cart_items.aggregate(
            total_quantity=ExpressionWrapper(
                Sum("quantity"), output_field=PositiveIntegerField()
            )
        )["total_quantity"]

    @property
    def total_price(self):
        """Calculate the total cost of items in the cart."""
        return self.cart_items.aggregate(
            total_price=Sum(
                ExpressionWrapper(
                    F("quantity") * F("price"), output_field=DecimalField()
                )
            )
        )["total_price"]
