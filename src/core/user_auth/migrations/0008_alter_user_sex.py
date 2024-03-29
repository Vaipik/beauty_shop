# Generated by Django 4.2.5 on 2024-01-09 14:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_auth", "0007_user_first_name_user_last_name_user_sex"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="sex",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("U", "Undefined")],
                default="U",
                max_length=1,
                verbose_name="Sex",
            ),
        ),
    ]
