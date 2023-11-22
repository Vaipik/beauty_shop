from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
from core.base.models import Base, TimeStampedBase
import decimal

User = get_user_model()


class ShoppingCart(Base, TimeStampedBase):
    """Describe cart."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def total_quantity(self):
        """Count the total number of items in the cart."""
        return self.cartitem_set.aggregate(total_quantity=Sum("quantity"))[
            "total_quantity"
        ]

    @property
    def total_price(self):
        """Calculate the total cost of goods in the cart."""
        cart_items = self.cartitem_set.all()
        return sum(item.cost for item in cart_items)


class CartItem(Base, TimeStampedBase):
    """Describe goods of cart."""

    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product}, price - {self.product.price}"

    @property
    def price(self) -> decimal.Decimal:
        """Display product price."""
        return self.product.price

    @property
    def cost(self) -> decimal.Decimal:
        """Calculate the total cost of good in the cart."""
        return self.quantity * self.price
