# Generated by Django 4.2.5 on 2024-01-05 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_auth", "0004_alter_user_is_superuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="Email address",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                unique=True,
                verbose_name="Mobile phone",
            ),
        ),
    ]
