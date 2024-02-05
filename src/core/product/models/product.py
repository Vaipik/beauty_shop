from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.base.models import Base, TimeStampedBase
from core.product import constants


class Currency(Base, TimeStampedBase):
    """Describe currency."""

    name = models.CharField(
        max_length=constants.CURRENCY_NAME_MAX_LENGTH, verbose_name=_("Name")
    )
    abbreviation = models.CharField(
        max_length=constants.CURRENCY_ABBREVIATION_MAX_LENGTH,
        verbose_name=_("abbreviation"),
    )

    class Meta:
        db_table = "currency"
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return self.abbreviation


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
        null=True,
        blank=True,
    )

    price = models.ManyToManyField(
        to="Currency",
        through="ProductCurrency",
        related_name="price_products",
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
        choices=ProductStatusChoices.choices,
        default=ProductStatusChoices.IN_STOCK,
    )
    sibling_name = models.CharField(  # The name that will be displayed at the card
        max_length=constants.PRODUCT_NAME_MAX_LENGTH,
        verbose_name=_("Sibling name"),
    )
    main_card = models.BooleanField(  # Is product must be main card.
        verbose_name=_("Main card"),
        null=False,
        blank=False,
    )
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
    siblings = models.ManyToManyField(
        to="self",
        related_name="sibling",
        symmetrical=False,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Product")

    def __str__(self) -> str:
        return f"{self.name}"


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
        db_table = "product_currency"
        verbose_name = _("Currency for product")
        verbose_name_plural = _("Currencies for product")
        constraints = [
            models.CheckConstraint(
                name="value_is_positive",
                check=Q(value__gt=0),
                violation_error_message=_("Value for price must be positive."),
            ),
        ]
