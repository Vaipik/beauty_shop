# Generated by Django 4.2.9 on 2024-02-18 11:25

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0018_alter_product_siblings"),
    ]

    operations = [
        migrations.CreateModel(
            name="Currency",
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
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "abbreviation",
                    models.CharField(max_length=3, verbose_name="abbreviation"),
                ),
            ],
            options={
                "verbose_name": "Currency",
                "verbose_name_plural": "Currencies",
                "db_table": "currencies",
            },
        ),
        migrations.CreateModel(
            name="ProductCurrency",
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
                    "value",
                    models.DecimalField(
                        decimal_places=2, max_digits=8, verbose_name="Value for price"
                    ),
                ),
            ],
            options={
                "verbose_name": "Currency for product",
                "verbose_name_plural": "Currencies for product",
                "db_table": "product_prices",
            },
        ),
        migrations.RemoveConstraint(
            model_name="product",
            name="price_is_positive",
        ),
        migrations.RemoveField(
            model_name="product",
            name="price",
        ),
        migrations.AddField(
            model_name="productcurrency",
            name="currency",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="currencies",
                to="product.currency",
                verbose_name="Currency",
            ),
        ),
        migrations.AddField(
            model_name="productcurrency",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_currencies",
                to="product.product",
                verbose_name="Product",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="price",
            field=models.ManyToManyField(
                related_name="products",
                through="product.ProductCurrency",
                to="product.currency",
            ),
        ),
        migrations.AddConstraint(
            model_name="productcurrency",
            constraint=models.CheckConstraint(
                check=models.Q(("value__gt", 0)),
                name="value_is_positive",
                violation_error_message="Value for price must be positive.",
            ),
        ),
    ]
