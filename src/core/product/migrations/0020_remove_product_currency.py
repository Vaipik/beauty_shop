# Generated by Django 4.2.7 on 2024-02-05 10:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0019_product_currency"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="currency",
        ),
    ]
