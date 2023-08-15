from uuid import UUID

from ..models import ProductOption


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
