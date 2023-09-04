# Generated by Django 4.2.4 on 2023-08-31 06:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
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
                    "first_name",
                    models.CharField(max_length=255, verbose_name="First name"),
                ),
                ("last_name", models.CharField(verbose_name="Last name")),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Email address"
                    ),
                ),
                ("sex", models.CharField(verbose_name="User gender")),
                ("address", models.CharField(verbose_name="Address")),
                (
                    "groups",
                    models.ManyToManyField(
                        related_name="profile_groups", to="auth.group"
                    ),
                ),
                (
                    "user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_profiles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        related_name="profile_user_permissions", to="auth.permission"
                    ),
                ),
            ],
            options={
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
                "db_table": "profiles",
            },
        ),
    ]