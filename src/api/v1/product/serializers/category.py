from rest_framework import serializers

from core.product.models import ProductCategory


class ProductCategoryCreateResponseSeriliazer(serializers.ModelSerializer):
    """Serializer to be used in response when category created."""

    class Meta:
        model = ProductCategory
        fields = ["id", "name"]

        [
            "cf45526c-ead2-42a0-a730-6510c9cbfa7b",
            "c6c74617-8e66-40b6-82fa-40abac1e6998",
            "99be1936-b592-4e93-bb63-e215de6aee95",
            "10936a6b-1e66-4576-a5bc-dd2dc5d7fecc",
            "9f475e16-4297-445b-9715-7d71afdab1a8",
            "6c1c060e-ce5c-499e-b905-66797410ce56",
            "4df55603-d77d-44ca-9506-15b02e3a4f0d",
            "a0322925-cd17-4965-be49-f1d05965f626",
            "72d7b1bf-76ba-4a1a-a779-05a3ca151216",
        ]
