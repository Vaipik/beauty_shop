from django_filters import rest_framework as filters

from ..models import Product


class ProductFilter(filters.FilterSet):
    """Used for querying ProductViewSet."""

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr="lte")
    manufacturer = filters.CharFilter(
        field_name="manufacturer__name", lookup_expr="iexact"
    )

    class Meta:  # noqa D106
        model = Product
        fields = ["status"]
