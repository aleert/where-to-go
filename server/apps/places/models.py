from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel


class Place(TimeStampedModel):

    title = models.CharField(_('title'), max_length=255)
    description_short = models.CharField(_('short description'), max_length=255, blank=True)
    description_long = models.TextField(_('description'))
    lat = models.FloatField(_('latitude'))
    lon = models.FloatField(_('longitude'))

    def __str__(self):
        return self.title
