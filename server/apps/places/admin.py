from __future__ import annotations

from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.db.models import QuerySet
from django.utils.html import format_html
from django.utils.translation import gettext as _

from server.apps.places.models import Image, Place


def get_image_html(self, image: QuerySet[Image]) -> str:
    """Helper function to add display image as custom admin field."""
    return format_html('<img src="{url}" style="max-height:{max_height};"/>'.format(
        url=image.location.url,
        max_height='200px',
    ),
    )


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    ordering = ('_order', )
    readonly_fields = ('image', )

    image = get_image_html
    image.short_description = _('Image')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):

    list_display = ('title', 'description_short', 'lat', 'lon')
    search_fields = ('title', )
    inlines = (ImageInline, )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'location', 'place', 'image')
    search_fields = ('place', )
    ordering = ('place', '_order')

    image = get_image_html
    image.short_description = _('Image')
