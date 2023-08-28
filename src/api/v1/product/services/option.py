from uuid import UUID

from django.db import transaction
from django.db.models import QuerySet

from core.product.models import ProductOption


def get_options_binded_to_products():
    """Return all options that are connected/binded to produtcs."""
    query = """
     SELECT parent.id, parent.name,
           jsonb_agg(
              jsonb_build_object('id', child.id, 'name', child.name)
           ) AS options
        FROM product_options AS parent
        LEFT JOIN product_options AS child
        ON child.path SIMILAR TO CONCAT(parent.path, '____')
        INNER JOIN product_options_m2m as m2m ON
        child.id = m2m.productoption_id
        GROUP BY parent.id, parent.name
    """

    raw_queryset = ProductOption.objects.raw(query)
    return raw_queryset


def get_product_options_in_category(category_id: UUID):
    """Get all options for products that are presented in given category."""
    query = """
         SELECT parent.id, parent.name,
           jsonb_agg(
              jsonb_build_object('id', child.id, 'name', child.name)
           ) AS options
        FROM product_options AS parent
        LEFT JOIN product_options AS child
        ON child.path SIMILAR TO CONCAT(parent.path, '____')
        INNER JOIN product_options_m2m AS m2m ON
        child.id = m2m.productoption_id
        INNER JOIN products AS p ON m2m.product_id = p.id
        INNER JOIN product_category_m2m AS cm2m ON p.id = cm2m.product_id
        WHERE cm2m.productcategory_id = %s
        GROUP BY parent.id, parent.name
        """
    raw_queryset = ProductOption.objects.raw(query, (category_id,))
    return raw_queryset


def create_root_option(name: str) -> ProductOption:
    """Create a root of options tree."""
    root_option = ProductOption.add_root(name=name)
    return root_option


def create_child_option(name: str, parent_id: UUID) -> ProductOption:
    """Add a new child option to existing parent option node."""
    parent_option = ProductOption.objects.get(pk=parent_id)
    child_option = parent_option.add_child(name=name)
    return child_option


@transaction.atomic
def patch_option(
    option: ProductOption, name: str | None = None, parent_id: UUID | None = None
) -> QuerySet[ProductOption]:
    """Perform a partial update of option.

    Change a name of a option if it was given and(or) move option to parent node
    if it was given.
    """
    if parent_id is not None:
        parent_node = ProductOption.objects.get(pk=parent_id)
        option.move(parent_node, pos="sorted-child")
        return ProductOption.get_root_nodes()
    if name is not None:
        option.name = name
        option.save()
    return ProductOption.get_tree(option)


@transaction.atomic
def delete_option(option: ProductOption) -> None:
    """Delete an option and it descendants from db."""
    option.delete()
