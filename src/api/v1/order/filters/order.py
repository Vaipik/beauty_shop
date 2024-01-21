from django_filters import rest_framework as filters

from core.order.models import Order


class OrderFilter(filters.FilterSet):
    """The class for order filtering."""

    status = filters.MultipleChoiceFilter(
        choices=Order.OrderStatus.choices,
    )
    username = filters.CharFilter(
        field_name="user__username",
        lookup_expr="icontains",
        label="Case-sensitive containment username.",
    )
    created_at = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="date",
        label="Exact date",
    )
    created = filters.DateTimeFromToRangeFilter(
        field_name="created_at",
        label="Range for lookup.",
    )
    updated_at = filters.DateTimeFilter(
        field_name="updated_at",
        lookup_expr="date",
        label="Exact date.",
    )
    updated = filters.DateTimeFromToRangeFilter(
        field_name="updated_at",
        label="Range for lookup.",
    )

    class Meta:
        model = Order
        fields = [
            "status",
            "created_at",
            "updated_at",
        ]
