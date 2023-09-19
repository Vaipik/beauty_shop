from django.db import models
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from core.product import constants
from core.base.models import Base


class ProductOption(Base, MP_Node):
    """Describe product options."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=constants.PRODUCT_CATEGORY_NAME_MAX_LENGTH,
    )
    node_order_by = ["name"]

    class Meta:
        db_table = "product_options"
        verbose_name = _("Product option")
        verbose_name_plural = _("Product options")

    def __str__(self) -> str:
        return self.name
