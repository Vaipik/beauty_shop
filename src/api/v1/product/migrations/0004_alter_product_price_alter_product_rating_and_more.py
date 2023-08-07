# Generated by Django 4.2.4 on 2023-08-03 17:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_alter_productimage_img_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                verbose_name="Price",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="rating",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=3,
                null=True,
                verbose_name="Rating",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="sku",
            field=models.PositiveIntegerField(
                unique=True, verbose_name="Stock keeping unit"
            ),
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("price__gte", 0), ("price__isnull", True), _connector="OR"
                ),
                name="price_is_positive",
                violation_error_message="Price must be positive or empty.",
            ),
        ),
    ]
