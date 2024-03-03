from django_filters import rest_framework as filters

from core.product.models import Product


class ProductFilter(filters.FilterSet):
    """Used for querying ProductViewSet."""

    min_price = filters.NumberFilter(
        field_name="product_items__price", lookup_expr="gte"
    )
    max_price = filters.NumberFilter(
        field_name="product_items__price", lookup_expr="lte"
    )
    min_rating = filters.NumberFilter(
        field_name="product_items__rating", lookup_expr="gte"
    )
    max_rating = filters.NumberFilter(
        field_name="product_items__rating", lookup_expr="lte"
    )
    manufacturer = filters.CharFilter(
        field_name="manufacturer__name", lookup_expr="iexact"
    )

    class Meta:
        model = Product
        fields = ["product_items__status", "is_luxury"]
