from django.db import models
from django.utils.translation import gettext_lazy as _

from .. import constants
from .base import Base, TimeStampedBase


class Product(Base, TimeStampedBase):
    """Describe product itself."""

    class ProductStatusChoices(models.TextChoices):
        """Enum for product status."""

        IN_STOCK = "I", _("In stock")
        OUT_OF_STOCK = "O", _("Out of stock")
        PENDING = "P", _("Expected")

    name = models.CharField(
        max_length=constants.PRODUCT_NAME_MAX_LENGTH, verbose_name=_("Name")
    )
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    rating = models.DecimalField(
        verbose_name=_("Rating"),
        max_digits=3,  # 4.99 / 5
        decimal_places=2,
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=3,  # 4.99 / 5
        decimal_places=2,
    )
    sku = models.PositiveIntegerField(verbose_name=_("Stock keeping unit"))
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=1,
        choices=ProductStatusChoices.choices,
        default=ProductStatusChoices.IN_STOCK,
    )
    manufacturer = models.ForeignKey(
        to="ProductManufacturer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_("Manufacturer"),
    )

    categories = models.ManyToManyField(
        to="ProductCategory",
        db_table="product_category_m2m",
        related_name="product_categories",
        blank=True,
    )
    options = models.ManyToManyField(
        to="ProductCategoryOption",
        related_name="product",
        db_table="product_options_m2m",
        blank=True,
    )

    class Meta:  # noqa D106
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Product")

    def __str__(self) -> str:
        return f"{self.name}"
