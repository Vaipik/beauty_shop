from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.base.models import Base, TimeStampedBase
from core.product import constants


class ProductCurrency(Base, TimeStampedBase):
    """Define price and link to currency and product."""

    currency = models.ForeignKey(
        to="Currency",
        on_delete=models.CASCADE,
        related_name="currencies",
        verbose_name=_("Currency"),
    )
    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        related_name="product_currencies",
        verbose_name=_("Product"),
    )
    value = models.DecimalField(
        verbose_name=_("Value for price"),
        max_digits=constants.PRODUCT_PRICE_MAX_DIGITS,
        decimal_places=2,
    )

    class Meta:
        db_table = "product_prices"
        verbose_name = _("Currency for product")
        verbose_name_plural = _("Currencies for product")
        constraints = [
            models.CheckConstraint(
                name="value_is_positive",
                check=Q(value__gt=0),
                violation_error_message=_("Value for price must be positive."),
            ),
        ]


class Currency(Base):
    """Describe currency."""

    name = models.CharField(
        max_length=constants.CURRENCY_NAME_MAX_LENGTH, verbose_name=_("Name")
    )
    abbreviation = models.CharField(
        max_length=constants.CURRENCY_ABBREVIATION_MAX_LENGTH,
        verbose_name=_("abbreviation"),
        unique=True,
    )

    class Meta:
        db_table = "currencies"
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return self.abbreviation
