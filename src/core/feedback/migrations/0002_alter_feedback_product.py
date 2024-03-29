# Generated by Django 4.2.9 on 2024-02-18 13:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "product",
            "0021_remove_product_categories_remove_product_created_at_and_more",
        ),
        ("feedback", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedbacks",
                to="product.productitem",
            ),
        ),
    ]
