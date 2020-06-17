from __future__ import annotations

from typing import List

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.utils.html import format_html
from django.utils.translation import gettext as _

from server.apps.places.models import Image, Place


class ImageOrderAdminForm(forms.ModelForm):
    """Assigns images order within Place."""

    assign_order = forms.CharField(
        max_length=100,
        help_text="Enter order of images in comma separated list, e.g. '0,1,2,3'",
        required=False,
    )

    class Meta:
        model = Place
        fields = '__all__'

    def save(self, commit=True):
        new_order = self.cleaned_data.get('assign_order', None)
        if new_order:
            self.instance.set_image_order(self.img_pks[new_pos] for new_pos in new_order)
        return super().save(commit=commit)

    def clean_assign_order(self) -> List[int]:
        assign_order = self.cleaned_data.get('assign_order', None)
        if assign_order:
            new_order = self._validate_assign_order(assign_order)
            # img_pks implicitly ordered by _order field
            # https://docs.djangoproject.com/en/3.0/ref/models/options/#django.db.models.Options.order_with_respect_to
            self.img_pks = Image.objects.filter(place=self.instance.pk).values_list('pk', flat=True)
            if any(order > len(self.img_pks) for order in new_order):
                err_msg = "Index can't exceed number of images minus one."
                raise ValidationError(_(err_msg), code='invalid')

            return new_order
        return []

    def _validate_assign_order(self, assign_order: str) -> List[int]:
        """
        Image order sanity checks not requiring db access.

        Args:
          assign_order: user inputed new image order.

        Returns:
          new images order to assign.

        Raises:
          ValidationError.
        """
        try:
            new_order = [int(num) for num in assign_order.split(',')]
        except ValueError:
            raise ValidationError(_('Only numbers allowed.'))

        if any(order < 0 for order in new_order):
            raise ValidationError(_('No negative positions allowed.'))

        if len(set(new_order)) != len(new_order):
            raise ValidationError(_('Ordering cannot contain repeated numbers.'))

        return new_order


def get_image_html(self, image: QuerySet[Image]) -> str:
    """Helper function to add display image as custom admin field."""
    return format_html('<img src="{url}" style="max-height:{max_height};"/>'.format(
        url=image.location.url,
        max_height='200px',
    ),
    )


class ImageInline(admin.TabularInline):
    model = Image
    ordering = ('_order', )
    readonly_fields = ('image', )

    image = get_image_html
    image.short_description = _('Image')


@admin.register(Place)
class UserAdmin(admin.ModelAdmin):

    list_display = ('title', 'description_short', 'lat', 'lon')
    search_fields = ('title', )
    inlines = (ImageInline, )
    form = ImageOrderAdminForm


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'location', 'place', 'image')
    search_fields = ('place', )

    image = get_image_html
    image.short_description = _('Image')
