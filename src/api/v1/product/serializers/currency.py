from rest_framework import serializers

from core.product.models import Currency, ProductCurrency


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for Currency model."""

    class Meta:
        model = Currency
        fields = ["id", "name", "abbreviation"]
        read_only_fields = ["id"]


class ProductCurrencySerializer(serializers.ModelSerializer):
    """Serializer for ProductCurrency model."""

    currencyId = serializers.UUIDField(source="currency_id", write_only=True)
    productId = serializers.UUIDField(source="product_id", write_only=True)
    name = serializers.CharField(source="currency.name")

    class Meta:
        model = ProductCurrency
        fields = ["id", "currencyId", "productId", "value", "name"]
        read_only_fields = ["id"]
