# Generated by Django 4.2.4 on 2023-08-31 11:24

from django.db import migrations, models
import uuid

from core.user_auth import managers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
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
                    "username",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Username"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        unique=True,
                        verbose_name="Email address",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, null=True, verbose_name="Phone number"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date of creation"
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                ("is_staff", models.BooleanField(default=False, verbose_name="Staff")),
                (
                    "is_superuser",
                    models.BooleanField(default=False, verbose_name="Verified"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "users",
                "db_table": "users",
                "unique_together": {("username", "email", "phone")},
            },
            managers=[
                ("objects", managers.UserManager()),
            ],
        ),
    ]
