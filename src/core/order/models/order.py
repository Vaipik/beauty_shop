from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base.models import Base, TimeStampedBase
from core.order import constants

User = get_user_model()


class Order(Base, TimeStampedBase):
    """User order model.

    Some fields are duplicated from user profile. This is neccessary to keep anonymous
    user possibility to perform an order.
    """

    class OrderStatus(models.TextChoices):
        """ENUM for order status."""

        NEW = 0, _("New")
        PROCESSING = 1, _("Processing")
        DELIVERY = 2, _("Delivery")
        SUCCESS = 3, _("Success")
        CANCELLED = 4, _("Cancelled")

    first_name = models.CharField(
        max_length=constants.FIRST_NAME_MAX_LENGTH,
        verbose_name=_("First name"),
        null=False,
    )
    last_name = models.CharField(
        max_length=constants.LAST_NAME_MAX_LENGTH,
        verbose_name=_("Last name"),
        null=False,
    )
    email = models.EmailField(
        max_length=255,
        verbose_name=_("Email address"),
        blank=True,
        null=True,
    )
    phone = models.CharField(
        max_length=10,  # 01234567890
        verbose_name=_("Mobile phone"),
        null=False,
    )
    status = models.PositiveSmallIntegerField(
        verbose_name=_("Status"),
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
    )
    is_paid = models.BooleanField(
        verbose_name=_("Paid"),
        default=False,
    )
    address = models.CharField()

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.last_name=} {self.first_name=} [{self.status=} {self.is_paid}]"
