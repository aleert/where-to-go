from contextlib import suppress

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = 'server.apps.users'
    verbose_name = _('Users')

    def ready(self):
        with suppress(ImportError):
            from server.apps.users import signals  # noqa: WPS433, F401
