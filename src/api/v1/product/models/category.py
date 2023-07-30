from django.db import models
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from .. import constants
from .base import Base


class ProductCategory(Base, MP_Node):
    """Store category by implementing Materialized Path pattern."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=constants.PRODUCT_CATEGORY_NAME_MAX_LENGTH,
    )
    node_order_by = ["name"]

    class Meta:  # noqa D106
        db_table = "product_categories"
        verbose_name = _("Product category")
        verbose_name_plural = _("Product categories")

    def __str__(self) -> str:
        return self.category

    @property
    def category(self):
        """To get all category with subcategories. Like cat1 / cat11 / cat 111."""
        return " / ".join([c.name for c in self.get_ancestors()])
