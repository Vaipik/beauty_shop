from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import (
    Product,
    ProductCategory,
    ProductCategoryOption,
    ProductManufacturer,
    ProductImage,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "rating", "sku")
    list_display_links = ("id", "name")
    filter_horizontal = ("categories",)
    search_fields = ("name", "description", "price", "rating", "sku")
    list_filter = ("name", "price", "sku")


@admin.register(ProductCategory)
class ProductCategoryAdmin(TreeAdmin):
    form = movenodeform_factory(ProductCategory)


@admin.register(ProductCategoryOption)
class ProductCategoryOptionAdmin(TreeAdmin):
    form = movenodeform_factory(ProductCategoryOption)


admin.site.register(ProductManufacturer)


admin.site.register(ProductImage)
