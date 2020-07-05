from server.settings.local import *

DATABASES['default'] = DATABASES['postgis']
DJANGO_APPS += ['django.contrib.gis']
