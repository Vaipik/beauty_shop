from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base.models import Base, TimeStampedBase


class ProductImage(Base, TimeStampedBase):
    """Store data about product images."""

    img_path = models.ImageField(
        verbose_name=_("Image path"),
        upload_to="%Y/%m/%d",
        null=False,
    )
    img_order = models.PositiveSmallIntegerField(verbose_name=_("Order"), null=True)
    product = models.ForeignKey(
        to="product.Product",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
    )

    class Meta:
        db_table = "product_images"
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
        unique_together = ("img_order", "product")
        ordering = ["img_order"]

    def __str__(self) -> str:
        return f"{self.product} №{self.img_order}"
