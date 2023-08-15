from django.db import models
from django.utils.translation import gettext_lazy as _

from core.product import constants
from .base import Base


class ProductManufacturer(Base):
    """Manufacturer model."""

    name = models.CharField(
        max_length=constants.PRODUCT_MANUFACTURER_NAME_MAX_LENGTH,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        null=True,
    )

    class Meta:  # noqa D106
        db_table = "manufacturers"
        verbose_name = _("Manufacturer")
        verbose_name_plural = _("Manufacturers")

    def __str__(self) -> str:
        return f"{self.name}"
