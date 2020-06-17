from urllib.parse import urljoin

from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.shortcuts import render

from server.apps.places.geojson_serializer import serialize_places
from server.apps.places.models import Place


def place_details_json(request, place_id: int):
    """Return json representation of place."""
    # have to pass iterable to serializer
    place = Place.objects.annotate(
        imgs=ArrayAgg('image__location', ordering=('image___order', )),
    ).values(
        'title', 'imgs', 'description_long', 'description_short', 'lon', 'lat',
    ).get(
        pk=place_id,
    )
    place['coordinates'] = [place['lon'], place['lat']]
    for idx, image in enumerate(place['imgs']):
        place['imgs'][idx] = urljoin(settings.MEDIA_URL, image)
    del place['lon'], place['lat']  # noqa:WPS420

    return JsonResponse(place)


def home(request):
    """Homepage with places geojson dicts in context."""
    geo_data = serialize_places(Place.objects.all())
    return render(request, template_name='pages/home.html', context={'geo_data': geo_data})
