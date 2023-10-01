from uuid import UUID

from django.db import transaction
from django.db.models import QuerySet

from core.product.models import ProductCategory


def get_categories_binded_to_products():
    """Return all categories that are connected/binded to products."""
    query = """
     SELECT parent.id, parent.name,
           jsonb_agg(
              jsonb_build_object('id', child.id, 'name', child.name)
           ) AS categories
        FROM product_categories AS parent
        LEFT JOIN product_categories AS child
        ON child.path SIMILAR TO CONCAT(parent.path, '____')
        INNER JOIN product_category_m2m as m2m ON
        child.id = m2m.productcategory_id
        GROUP BY parent.id, parent.name
    """

    raw_queryset = ProductCategory.objects.raw(query)

    return raw_queryset


def create_root_category(name: str) -> ProductCategory:
    """Create a root of categories tree."""
    root_category = ProductCategory.add_root(name=name)
    return root_category


def create_child_category(name: str, parent_id: UUID) -> ProductCategory:
    """Add a new child category to existing parent category node."""
    parent_category = ProductCategory.objects.get(pk=parent_id)
    child_category = parent_category.add_child(name=name)
    return child_category


@transaction.atomic
def update_category(
    category: ProductCategory,
    name: str | None,
    parent_id: UUID | None,
    to_root: bool,
) -> QuerySet[ProductCategory]:
    """Perform a partial update of category.

    Change a name of a category if it was given and(or) move category to parent node
    if it was given.
    """
    _change_category_name(category, name)

    if to_root:
        root = category.get_root()
        category.move(root)
        return ProductCategory.get_root_nodes()

    if parent_id is not None:
        parent_node = ProductCategory.objects.get(pk=parent_id)
        category.move(parent_node, pos="sorted-child")
        return ProductCategory.get_root_nodes()

    return ProductCategory.get_tree(category)


@transaction.atomic
def delete_category(category: ProductCategory) -> None:
    """Delete a category and it descendants from db."""
    category.delete()


def _change_category_name(category: ProductCategory, name: str | None) -> None:
    """If name was provided and it is not equal to current name it will be updated."""
    if name:
        if category.name != name:
            category.name = name
            category.save()


def bind_option_to_category(pk: UUID, option_id: UUID) -> None:
    """Attach given option to a category."""
    category = ProductCategory.objects.get(pk=pk)
    category.options.add(option_id)


def remove_option_from_category(pk: UUID, option_id: UUID) -> None:
    """Remove attached option from a category."""
    category = ProductCategory.objects.get(pk=pk)
    category.options.remove(option_id)
