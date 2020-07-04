"""Postgres point filed, related lookup and widgets."""
import numbers
from dataclasses import dataclass
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Lookup
from django.forms.fields import FloatField, MultiValueField
from django.forms.widgets import MultiWidget, TextInput
from django.utils.translation import gettext_lazy as _


@dataclass
class Point:
    """Coordinate point with lontitude and latitude."""

    lon: numbers.Real
    lat: numbers.Real

    def __getitem__(self, item):
        """
        Support getting lon, lat with 0,1 indexes.

        Provides compatibility with tuple syntax.
        """
        return (self.lon, self.lat)[item]


class PointField(models.Field):

    def db_type(self, connection: Any) -> str:
        return 'point'

    def get_prep_value(self, value: Any) -> Any:
        if not value:
            return value
        return f'{value[0], value[1]}'

    def from_db_value(self, value, expression, connection) -> Any:
        if value is None:
            return value
        return Point(
            *(float(coord) for coord in value[1:-1].split(',')),
        )

    def to_python(self, value: Any) -> Any:
        if isinstance(value, (tuple, Point)):
            return value
        if value is None:
            return None
        return Point(
            *(float(coord) for coord in value[1:-1].split(',')),
        )

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': MyFormField, **kwargs}
        return super().formfield(**defaults)


@PointField.register_lookup
class InBoxLookup(Lookup):
    """
    Lookup for points contained in box.

    Box defined by a tuple of two opposite angle points, either of which can be
    Point instance or (lng, lat) tuple.
    """

    lookup_name = 'contained_in'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)  # noqa:WPS323
        all_params = lhs_params + rhs_params
        return '%s <@ box %s' % (lhs, rhs), all_params

    def get_prep_lookup(self):
        """Reimplement for tuple of Points instead of single point."""
        if hasattr(self.rhs, 'resolve_expression'):  # noqa:WPS421
            return self.rhs
        if self.prepare_rhs and hasattr(self.lhs.output_field, 'get_prep_value'):  # noqa:WPS421
            return ', '.join([
                self.lhs.output_field.get_prep_value(self.rhs[0]),
                self.lhs.output_field.get_prep_value(self.rhs[1]),
            ])
        return self.rhs


class SplitPointWidget(MultiWidget):
    """Split lng and lat in separate boxes."""

    def __init__(self, attrs=None):
        lng_attrs = {'placeholder': 'lng'}
        lat_attrs = {'placeholder': 'lat'}
        if attrs:
            lng_attrs.update(attrs)
            lat_attrs.update(attrs)
        widgets = (
            TextInput(attrs=lng_attrs),
            TextInput(attrs=lat_attrs),
        )
        super().__init__(widgets)

    def decompress(self, value):  # noqa:WPS110
        if value:
            return [value.lon, value.lat]
        return [None, None]


class MyFormField(MultiValueField):
    widget = SplitPointWidget
    default_error_messages = {
        'invalid_lng': _('Enter a valid longitude.'),
        'invalid_lat': _('Enter a valid latitude.'),
    }

    def __init__(self, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs.get('error_messages', {}))
        localize = kwargs.get('localize', False)
        fields = (
            FloatField(
                label='lng',
                error_messages={'invalid': errors['invalid_lng']},
                localize=localize,
            ),
            FloatField(
                label='lat',
                error_messages={'invalid': errors['invalid_lat']},
                localize=localize,
            ),
        )
        super().__init__(fields, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in self.empty_values:
                raise ValidationError(self.error_messages['invalid_lng'], code='invalid_coord')
            if data_list[1] in self.empty_values:
                raise ValidationError(self.error_messages['invalid_lat'], code='invalid_lat')
            return Point(data_list[0], data_list[1])
        return None
