from django.apps import AppConfig


class BursaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Bursary'

    def ready(self):
        import Bursary.signals
