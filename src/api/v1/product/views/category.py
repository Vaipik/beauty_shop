from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.product.models import ProductCategory
from api.v1.product import swagger_examples
from ..serializers import (
    ProductCategoryCreateRequestSeriliazer,
    ProductCategoryCreateResponseSeriliazer,
    ProductCategoryListResponseSerializer,
    ProductOptionListResponseSerializer,
    ProductListResponseSerializer,
)
from .. import services


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """Viewset for categories that are binded for products."""

    serializer_class = ProductCategoryListResponseSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        """Choose which queryset should be queried."""
        if self.action == "list":
            return ProductCategory.get_root_nodes()
        if self.action == "retrieve":
            node = ProductCategory.objects.get(pk=self.kwargs["pk"])
            return ProductCategory.get_tree(node)
        if self.action == "products":
            return services.get_products_for_category(self.kwargs["pk"])
        if self.action == "options":
            return services.get_product_options_in_category(self.kwargs["pk"])
        return super().get_queryset()

    def get_serializer_class(self):  # noqa D102
        if self.action == "create":
            return ProductCategoryCreateRequestSeriliazer
        return super().get_serializer_class()

    @extend_schema(
        description="This endpoint is used to create a category and subcategories for "
        "products. If you want to create a root of your categories tree you "
        "don't need to pass a parentId, leave it NULL. If you want to"
        "create a subcategory than you need to provide a parentId of category"
        "and provide a name for subcategory.",
        request=ProductCategoryCreateRequestSeriliazer,
        responses=ProductCategoryCreateResponseSeriliazer,
        examples=swagger_examples.get_created_tree_examples(),
    )
    def create(self, request, *args, **kwargs):  # noqa D102
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if parent_id := serializer.data.get("parent_id"):
            category = services.create_child_category(
                serializer.data["name"], parent_id
            )
        else:
            category = services.create_root_category(serializer.data["name"])

        response = ProductCategoryCreateResponseSeriliazer(category)
        return Response(data=response.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Provide all categories that are presented."
        "Note that depth are not limited.",
        examples=swagger_examples.get_nested_examples(),
    )
    def list(self, request, *args, **kwargs):  # noqa D102
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Provide all categories that are presented in given category."
        "Note that depth are not limited.",
        examples=swagger_examples.get_nested_examples(),
    )
    def retrieve(self, request, *args, **kwargs):  # noqa D102
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses=ProductListResponseSerializer(many=True),
        description="List of products for category.",
    )
    @action(
        detail=True, methods=["get"], serializer_class=ProductListResponseSerializer
    )
    def products(self, request, pk=None):
        """Extra route to obtain list of products for a category."""
        queryset = self.get_queryset()
        serialzer = self.get_serializer(queryset, many=True)
        return Response(serialzer.data, status=200)

    @extend_schema(
        responses=ProductOptionListResponseSerializer(many=True),
        description="List of product options that are presented in category.",
    )
    @action(
        detail=True,
        methods=["get"],
        serializer_class=ProductOptionListResponseSerializer,
    )
    def options(self, request, pk=None):
        """Extra route to obtain list of products for a category."""
        queryset = self.get_queryset()
        serialzer = self.get_serializer(queryset, many=True)
        return Response(serialzer.data, status=200)
