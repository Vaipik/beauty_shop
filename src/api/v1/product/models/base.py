from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    """Base model to define UUID as primary key."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )

    class Meta:  # noqa D106
        abstract = True


class TimeStampedBase(models.Model):
    """Add extra fields for created and updated."""

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True,
    )

    class Meta:  # noqa D106
        abstract = True
