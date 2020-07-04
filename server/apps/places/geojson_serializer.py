"""
Utility to convert Place queryset into frontent-compatible GEOJson.

Does not require GeoDjango setup or DRF, but not really flexible.
"""
from __future__ import annotations

from typing import Dict

from django.db.models import QuerySet
from django.urls import reverse
from slugify import slugify

from server.apps.places.models import Place


def serialize_places(places: QuerySet[Place]) -> Dict:
    """Serialize places queryset into geo_dict to be converted to json."""
    places = places.values()

    features = [_place_to_feature(place) for place in places]

    return {
        'type': 'FeatureCollection',
        'features': features,
    }


def _place_to_feature(place: Dict) -> Dict:
    """
    Convert dict representation of Place to GeoJSON feature object.

    Feature object specs: https://tools.ietf.org/html/rfc7946#section-3.2
    """
    return {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [place['coord'].lon, place['coord'].lat],
        },
        'properties': {
            'title': place['title'],
            'placeId': slugify(place['title']),
            'detailsUrl': reverse('places:place-details-json', kwargs={'place_id': place['id']}),
        },
    }
