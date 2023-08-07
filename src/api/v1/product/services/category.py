from ..models import ProductCategory


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
