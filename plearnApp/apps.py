from django.apps import AppConfig


class PlearnappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plearnApp'

    def ready(self):
        import plearnApp.signals