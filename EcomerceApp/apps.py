from django.apps import AppConfig


class EcomerceappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EcomerceApp'

    def ready(self):
        import EcomerceApp.signals 
