"""With these settings, tests run faster."""

from server.settings.base import *  # noqa: WPS347
from server.settings.base import config

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = config('DJANGO_SECRET_KEY')
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
    },
}

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[-1]['OPTIONS']['loaders'] = [  # type: ignore[index] # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
    ),
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Your stuff...
# ------------------------------------------------------------------------------
