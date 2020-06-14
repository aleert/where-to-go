import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import DEFAULT_DB_ALIAS
from psycopg2 import OperationalError


class Command(BaseCommand):
    """
    Django command to pause execution until db is available.

    Note that you can't use db_conn_wrapper.is_usable() because
    django.db.backends.postgresql.base.py DatabaseWrapper
    behaves strange and do not create cursor for self.cursor(),
    returning None instead.
    Using django.db.connection.ensure_connection() as in
    https://stackoverflow.com/questions/32098797/how-can-i-check-database-connection-to-mysql-in-django
    also a bad idea as it hangs python completely.
    """

    requires_system_checks = False

    def handle(self, *args, **options):  # noqa: WPS110
        self.stdout.write('Waiting for database...')

        db_conn_wrapper = connections[DEFAULT_DB_ALIAS]
        db_conn = None

        while not db_conn:
            try:
                db_conn = db_conn_wrapper.get_new_connection(
                    db_conn_wrapper.get_connection_params(),
                )
            except OperationalError:
                self.stdout.write('Database unavailable. Waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available.'))
