from rest_framework import serializers

from api.base.serializers import TimeStampedSerializer
from core.product import constants
from core.product.models.currency import Currency, ProductCurrency


class CurrencySerializer(TimeStampedSerializer, serializers.ModelSerializer):
    """Serializer for Currency model."""

    class Meta:
        model = Currency
        fields = "__all__"
        read_only_fields = ["id", "createdAt", "updatedAt"]


class ProductCurrencySerializer(serializers.ModelSerializer):
    """Serializer for ProductCurrency model."""

    currencyId = serializers.UUIDField(required=False, source="currency_id")
    productId = serializers.UUIDField(required=False, source="product_id")
    value = serializers.DecimalField(
        required=False,
        max_digits=constants.PRODUCT_PRICE_MAX_DIGITS,
        decimal_places=2,
    )

    class Meta:
        model = ProductCurrency
        fields = ["id", "currencyId", "productId", "value"]
        read_only_fields = ["id", "currencyId", "productId"]
