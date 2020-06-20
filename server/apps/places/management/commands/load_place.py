import tempfile
from typing import Iterable

import requests
from django.core import files
from django.core.management.base import BaseCommand, CommandParser
from django.db.transaction import atomic
from tqdm import tqdm

from server.apps.places.models import Image, Place


class Command(BaseCommand):
    """Loads Place json from remote source and save it to database."""

    requires_system_checks = True
    help = 'Pass a json web address as the first argument.'  # noqa: WPS125

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('place_url')

    @atomic
    def handle(self, *args, **options):  # noqa: WPS110
        try:
            place_json = requests.get(options['place_url'])
        except requests.exceptions.RequestException as err:
            self.stderr.write(str(err))
            return

        if place_json.status_code != requests.status_codes.codes.ok:
            self.stderr.write(f'Get status code {place_json.status_code}, exiting.')
            return

        place_json = place_json.json()
        place, created = Place.objects.get_or_create(
            title=place_json['title'],
            lon=float(place_json['coordinates']['lng']),
            lat=(place_json['coordinates']['lat']),
            defaults={
                'description_short': place_json['description_short'],
                'description_long': place_json['description_long'],
            },
        )

        if not created:
            self.stderr.write('Place already exists, exiting..')
            return

        self.stdout.write('Loaded new place ...')
        self._save_images(images=place_json['imgs'], place=place)
        self.stdout.write('Place uploaded successfully', style_func=self.style.SUCCESS)

    def _save_images(self, images: Iterable, place: Place):  # noqa: C901, WPS231
        """Loads images and saves them to ``place``."""
        for img_url in tqdm(images, desc='Processing images: ', file=self.stdout):
            image_file = ''
            try:
                image_file = requests.get(img_url, stream=True)
            except requests.exceptions.RequestException:
                self.stderr.write(f'Cannot get {img_url}. Skipping..')

            if image_file:
                tmp_img = tempfile.NamedTemporaryFile()

                for block in image_file.iter_content(1024 * 8):
                    if not block:
                        break  # noqa: WPS220
                    tmp_img.write(block)

                new_img = Image(place=place)
                new_img.location.save(img_url.split('/')[-1], files.File(tmp_img))  # noqa: WPS221
