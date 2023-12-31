# Generated by Django 4.2.5 on 2023-10-14 07:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0017_alter_product_siblings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="siblings",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="sibling", to="product.product"
            ),
        ),
    ]
