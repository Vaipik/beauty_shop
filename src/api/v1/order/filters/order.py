from django_filters import rest_framework as filters

from core.order.models import Order


class OrderFilter(filters.FilterSet):
    """The class for order filtering."""

    status = filters.CharFilter(field_name="status", lookup_expr="iexact")
    # status = filters.ChoiceFilter(choices=Order.OrderStatus.choices)
    user = filters.CharFilter(field_name="user__username", lookup_expr="iexact")
    created_date = filters.DateTimeFilter(field_name="created_at", lookup_expr="date")
    created_range = filters.DateTimeFromToRangeFilter(
        field_name="created_at",
    )
    updated_date = filters.DateTimeFilter(field_name="updated_at", lookup_expr="date")
    updated_range = filters.DateTimeFromToRangeFilter(
        field_name="updated_at",
    )

    class Meta:
        model = Order
        fields = [
            "status",
            "user",
            "created_date",
            "created_range",
            "updated_date",
            "updated_range",
        ]
