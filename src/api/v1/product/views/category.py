from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.base.permissions import StaffPermission
from api.v1.product import services, swagger_examples
from api.v1.product.filters import ProductFilter
from api.v1.product.serializers import (
    ProductCategoryCreateResponseSeriliazer,
    ProductOptionBindedSerializer,
    ProductSerializer,
    TreeCreateUpdateSerializer,
    TreeListResponseSerializer,
)
from api.v1.product.serializers.common import UUIDListSerializer
from core.product.models import ProductCategory


# noinspection PyTestUnpassedFixture
class ProductCategoryViewSet(viewsets.ModelViewSet):
    """Viewset for categories that are binded for products."""

    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        """To use a custom permissions."""
        if self.action in {"create", "partial_update", "destroy"}:
            permission_classes = [StaffPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Choose which queryset should be queried."""
        if getattr(self, "swagger_fake_view", False):  # drf-yasg comp
            return ProductCategory.objects.none()
        if self.action == "list":
            return ProductCategory.get_root_nodes()
        if self.action == "retrieve":
            node = ProductCategory.objects.get(pk=self.kwargs["pk"])
            return ProductCategory.get_tree(node)
        if self.action in {"partial_update", "destroy", "bind_options_delete"}:
            return ProductCategory.objects.get(pk=self.kwargs["pk"])
        if self.action == "products":
            return services.get_products_for_category(self.kwargs["pk"])
        if self.action == "options":
            return services.get_product_options_in_category(self.kwargs["pk"])
        if self.action == "bind_options":
            return services.get_options_binded_to_category(self.kwargs["pk"])
        return super().get_queryset()

    def get_serializer_class(self):
        """Choose serializer for input data."""
        if self.action in {"create", "partial_update"}:
            return TreeCreateUpdateSerializer
        if self.action == "list":
            return TreeListResponseSerializer
        if self.action == "bind_options":
            return ProductOptionBindedSerializer
        return super().get_serializer_class()

    @extend_schema(
        description="This endpoint is used to create a category and subcategories for "
        "products. If you want to create a root of your categories tree you "
        "don't need to pass a parentId, leave it NULL. If you want to"
        "create a subcategory than you need to provide a parentId of category"
        "and provide a name for subcategory.",
        request=TreeCreateUpdateSerializer,
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

        if parent_id := serializer.data.get("parentId"):
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
        responses=TreeListResponseSerializer(many=True),
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
        description="This endpoint is used to make a partial update of option."
        " E.g change option name or move it to another parent option"
        " with all its children. If you want only to change name leave"
        " parent id empty, if you want to move option provide parent id.",
        request=TreeCreateUpdateSerializer,
        responses=TreeListResponseSerializer,
        examples=swagger_examples.update_tree_example(),
    )
    def partial_update(self, request, *args, **kwargs):
        """PATCH for the category. Can be removed to another parent or renamed."""
        instance = self.get_queryset()
        request_serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        request_serializer.is_valid(raise_exception=True)
        update_cat = services.update_category(
            category=instance,
            name=request.data.get("name"),
            parent_id=request.data.get("parentId"),
            to_root=request.data.get("toRoot", False),
        )
        if request.data.get("parentId") or request.data.get("toRoot"):
            response_serializer = TreeListResponseSerializer(update_cat, many=True)
        else:
            instance.refresh_from_db()
            response_serializer = TreeListResponseSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete the category and its descendants."""
        instance = self.get_queryset()
        services.delete_category(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses=ProductSerializer(many=True),
        parameters=swagger_examples.get_parameters(),
    )
    @action(
        detail=True,
        methods=["get"],
        serializer_class=ProductSerializer,
    )
    def products(self, request, *args, **kwargs):
        """Extra route to obtain list of products for a category."""
        products = self.get_queryset()
        filterset = ProductFilter(data=request.query_params, queryset=products)
        serialzer = self.get_serializer(filterset.qs, many=True)
        return Response(serialzer.data, status=200)

    @extend_schema(
        responses=TreeListResponseSerializer(many=True),
        description="List of product options that are presented in products for given"
        " category.",
    )
    @action(
        detail=True,
        methods=["get"],
        serializer_class=TreeListResponseSerializer,
    )
    def options(self, request, pk: UUID = None):
        """Extra route to obtain list of products for a category."""
        queryset = self.get_queryset()
        serialzer = self.get_serializer(queryset, many=True)
        return Response(serialzer.data, status=200)

    @extend_schema(
        description="List of binded product options.",
        responses=UUIDListSerializer,
        request=UUIDListSerializer,
    )
    @action(
        detail=True,
        methods=["get", "post"],
        url_path=r"bind_options",
    )
    def bind_options(self, request, pk: UUID = None):
        """Get attached options to category."""
        if request.method == "GET":
            queryset = self.get_queryset()
            response = self.get_serializer(queryset, many=True)
            ids = [item["id"] for item in response.data]
            return Response(ids, status=200)
        if request.method == "POST":
            serializer = UUIDListSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            services.bind_option_to_category(pk, serializer.data)
            response = self.get_serializer(
                services.get_options_binded_to_category(pk), many=True
            )
            ids = [item["id"] for item in response.data]
            return Response(ids, status=201)

    @action(
        detail=True,
        methods=["delete"],
        url_path=r"bind_options/(?P<option_id>[^/.]+)",
    )
    def bind_options_delete(self, request, pk: UUID, option_id: UUID):
        """Remove attached options from a category."""
        services.remove_option_from_category(pk, option_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
