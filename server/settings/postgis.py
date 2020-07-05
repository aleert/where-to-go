from server.settings.local import *

DATABASES['default'] = DATABASES['postgis']
DJANGO_APPS += ['django.contrib.gis']
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
