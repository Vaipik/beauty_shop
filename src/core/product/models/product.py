from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from core.product import constants
from core.base.models import Base, TimeStampedBase


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
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=constants.PRODUCT_PRICE_MAX_DIGITS,
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
        constraints = [
            models.CheckConstraint(
                name="price_is_positive",
                check=Q(price__gte=0) | Q(price__isnull=True),
                violation_error_message=_("Price must be positive or empty."),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name}"
