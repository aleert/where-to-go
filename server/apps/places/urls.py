from django.urls import path

from server.apps.places.views import place_details_json, points

app_name = 'places'

urlpatterns = [
    path(
        'place-details/<int:place_id>/',
        view=place_details_json,
        name='place-details-json',
    ),
    path(
        'points/',
        view=points,
        name='points',
    ),
]
