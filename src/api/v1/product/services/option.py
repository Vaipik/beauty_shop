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
