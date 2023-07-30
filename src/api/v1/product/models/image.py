from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import Base, TimeStampedBase


class ProductImage(Base, TimeStampedBase):
    """Store data about product images."""

    img_path = models.FileField(
        verbose_name=_("Image path"),
        upload_to="%Y/%m/%d",
        null=False,
    )
    img_order = models.PositiveSmallIntegerField(verbose_name=_("Order"), null=False)
    product = models.ForeignKey(
        to="product.Product",
        on_delete=models.CASCADE,
        related_name="images",
        null=False,
    )

    class Meta:  # noqa D106
        db_table = "product_images"
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
        unique_together = ("img_order", "product")

    def __str__(self) -> str:
        return f"{self.product.name} №{self.img_order}"
