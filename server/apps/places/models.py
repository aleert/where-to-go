from django.contrib.postgres.indexes import GistIndex
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from server.apps.places.fields import PointField


class Place(models.Model):

    title = models.CharField(_('title'), max_length=255)  # noqa: WPS432
    description_short = models.CharField(
        _('short description'), max_length=1000, blank=True,
    )
    description_long = HTMLField(_('description'))
    coord = PointField(_('coordinates (lng, lat)'))

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        indexes = (
            GistIndex(fields=['coord']),
        )

    def __str__(self):
        return self.title


class Image(models.Model):

    location = models.ImageField(_('Image location'), upload_to='places/%Y/%m')
    place = models.ForeignKey(to='Place', on_delete=models.CASCADE)
    _order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('_order', )
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        pattern = _('Picture {order} of Place {title}')
        return pattern.format(order=self._order, title=self.place.title)
