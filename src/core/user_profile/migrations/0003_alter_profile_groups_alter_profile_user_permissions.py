# Generated by Django 4.2.4 on 2023-08-31 06:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("user_profile", "0002_alter_profile_groups_alter_profile_user_permissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="groups",
            field=models.ManyToManyField(
                blank=True, related_name="profile_groups", to="auth.group"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                related_name="profile_user_permissions",
                to="auth.permission",
            ),
        ),
    ]
