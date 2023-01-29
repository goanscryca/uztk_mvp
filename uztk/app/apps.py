from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "uztk.app"
    verbose_name = _("App")

    def ready(self):
        try:
            import uztk.app.signals  # noqa F401
        except ImportError:
            pass
