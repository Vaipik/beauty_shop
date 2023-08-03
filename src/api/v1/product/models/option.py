from django.db import models
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from .. import constants
from .base import Base


class ProductCategoryOption(Base, MP_Node):
    """Describe options specifically to a category."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=constants.PRODUCT_CATEGORY_NAME_MAX_LENGTH,
    )
    category = models.ForeignKey(
        to="ProductCategory",
        on_delete=models.DO_NOTHING,
        related_name="options",
    )
    node_order_by = ["name"]

    class Meta:  # noqa D106
        db_table = "product_category_options"
        verbose_name = _("Product category option")
        verbose_name_plural = _("Product category options")

    def __str__(self) -> str:
        return self.option

    @property
    def option(self):
        """To get all category with subcategories. Like cat1 / cat11 / cat 111."""
        # ancestors = self.get_ancestors()
        return self.name
