from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.cart"
    label = "api_v1_cart"

    def ready(self):
        import api.v1.cart.signals
