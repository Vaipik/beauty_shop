from django.apps import AppConfig


class ProfileAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.user_profile"

    def ready(self):
        pass
