from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(pre_save, sender=User)
def set_is_active_to_true(sender, instance, **kwargs):
    """Change is_active from False to True."""
    if instance.is_active is False:
        instance.is_active = True
