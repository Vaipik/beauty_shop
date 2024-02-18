from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base.models import Base, TimeStampedBase
from core.product import constants


class Product(Base):
    """Describe product and its items."""

    name = models.CharField(
        max_length=constants.PRODUCT_NAME_MAX_LENGTH, verbose_name=_("Name")
    )
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    is_luxury = models.BooleanField(
        verbose_name=_("Luxury"),
        null=False,
        blank=False,
        default=False,
    )
    manufacturer = models.ForeignKey(
        to="ProductManufacturer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_("Manufacturer"),
    )

    class Meta:
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Product")

    def __str__(self) -> str:
        return f"{self.name}"


class ProductItem(Base, TimeStampedBase):
    """Provide detailed data about product item."""

    class ProductItemStatusChoices(models.TextChoices):
        """Enum for product status."""

        IN_STOCK = "I", _("In stock")
        OUT_OF_STOCK = "O", _("Out of stock")
        PENDING = "P", _("Expected")

    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    name = models.CharField(
        max_length=constants.PRODUCT_ITEM_NAME_MAX_LENGTH, verbose_name=_("Item name")
    )
    price = models.ManyToManyField(
        to="Currency",
        through="ProductCurrency",
        related_name="products",
    )
    rating = models.DecimalField(
        verbose_name=_("Rating"),
        max_digits=3,  # 4.99 / 5
        decimal_places=2,
        null=True,
        blank=True,
    )
    sku = models.PositiveIntegerField(
        verbose_name=_("Stock keeping unit"),
        unique=True,
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=1,
        choices=ProductItemStatusChoices.choices,
        default=ProductItemStatusChoices.IN_STOCK,
    )

    product = models.ForeignKey(
        to="Product", on_delete=models.CASCADE, related_name="product_items"
    )

    categories = models.ManyToManyField(
        to="ProductCategory",
        db_table="product_category_m2m",
        related_name="product_categories",
        blank=True,
    )
    options = models.ManyToManyField(
        to="ProductOption",
        related_name="product",
        db_table="product_options_m2m",
        blank=True,
    )

    class Meta:
        db_table = "product_items"
        verbose_name = _("Product item")
        verbose_name_plural = _("Product items")
