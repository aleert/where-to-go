from urllib.parse import urljoin

from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.shortcuts import render

from server.apps.places.fields import Point
from server.apps.places.geojson_serializer import serialize_places
from server.apps.places.models import Place


def place_details_json(request, place_id: int):
    """Return json representation of place."""
    # have to pass iterable to serializer
    place = Place.objects.annotate(
        imgs=ArrayAgg('image__location', ordering=('image___order', )),
    ).values(
        'title', 'imgs', 'description_long', 'description_short', 'coord',
    ).get(
        pk=place_id,
    )
    place['coordinates'] = [place['coord'].lon, place['coord'].lat]
    for idx, image in enumerate(place['imgs']):
        place['imgs'][idx] = urljoin(settings.MEDIA_URL, image)
    del place['coord']  # noqa:WPS420

    return JsonResponse(place)


def home(request):
    """Homepage with places geojson dicts in context."""
    return render(request, template_name='pages/home.html')


def points(request):
    p1 = Point(
        *(float(coord) for coord in request.GET['up_right'].split(',')),
    )
    p2 = Point(
        *(float(coord) for coord in request.GET['low_left'].split(',')),
    )
    qs = Place.objects.filter(coord__contained_in=(
        (p1.lon, p1.lat), (p2.lon, p2.lat),
    )).all()
    return JsonResponse(serialize_places(qs))
