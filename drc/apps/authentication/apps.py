from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    """Triggers Profile creation through Signal"""

    name = 'drc.apps.authentication'

    def ready(self):
        import drc.apps.authentication.signals
