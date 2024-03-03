# Generated by Django 4.2.9 on 2024-02-18 12:30

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0020_alter_currency_abbreviation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="categories",
        ),
        migrations.RemoveField(
            model_name="product",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="product",
            name="main_card",
        ),
        migrations.RemoveField(
            model_name="product",
            name="options",
        ),
        migrations.RemoveField(
            model_name="product",
            name="price",
        ),
        migrations.RemoveField(
            model_name="product",
            name="rating",
        ),
        migrations.RemoveField(
            model_name="product",
            name="sibling_name",
        ),
        migrations.RemoveField(
            model_name="product",
            name="siblings",
        ),
        migrations.RemoveField(
            model_name="product",
            name="sku",
        ),
        migrations.RemoveField(
            model_name="product",
            name="status",
        ),
        migrations.RemoveField(
            model_name="product",
            name="updated_at",
        ),
        migrations.CreateModel(
            name="ProductItem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                ("name", models.CharField(max_length=256, verbose_name="Item name")),
                (
                    "rating",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=3,
                        null=True,
                        verbose_name="Rating",
                    ),
                ),
                (
                    "sku",
                    models.PositiveIntegerField(
                        unique=True, verbose_name="Stock keeping unit"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("I", "In stock"),
                            ("O", "Out of stock"),
                            ("P", "Expected"),
                        ],
                        default="I",
                        max_length=1,
                        verbose_name="Status",
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True,
                        db_table="product_category_m2m",
                        related_name="product_categories",
                        to="product.productcategory",
                    ),
                ),
                (
                    "options",
                    models.ManyToManyField(
                        blank=True,
                        db_table="product_options_m2m",
                        related_name="product",
                        to="product.productoption",
                    ),
                ),
                (
                    "price",
                    models.ManyToManyField(
                        related_name="products",
                        through="product.ProductCurrency",
                        to="product.currency",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_items",
                        to="product.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product item",
                "verbose_name_plural": "Product items",
                "db_table": "product_items",
            },
        ),
        migrations.AlterField(
            model_name="productcurrency",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_currencies",
                to="product.productitem",
                verbose_name="Product",
            ),
        ),
        migrations.AlterField(
            model_name="productimage",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="product.productitem",
            ),
        ),
    ]