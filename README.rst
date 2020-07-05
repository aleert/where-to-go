=============================
Stress testing with PostGIS
=============================

This branch intended for comparing performance for query that select
Place models based on their coordinates being contained in some geometric box.

Setup
=====

There are two setups to compare:

#.
  Regular postgres with custom field on django side, interfacing postgres
  ``point`` field and custom django lookup implementing ``WHERE point (x, y) <@ box (coords)``.

  There's also a ``GistIndex`` created with point field to increase above mentioned
  lookup performance. For further details refer to ``fields.py`` and ``models.PurePostgresPlace``
  in ``places`` app.

  (This setup based on ``progressive-loading`` branch)

#.
  This setup have ``PostGIS`` enabled and utilizes ``GeoDjango`` capabilities.

Host machine configuration
==========================

Debian 10 with Postgresql 12 installed, 8gb RAM, Intel Core i5-8250U

This project uses python 3.8.2 with django 3.0.7 and psycopg2 builded with --no-binary option.
Other packages can be viewed in ``requirements/local.txt`` and ``requirements/base.txt``.

Results
=======


I want to do it myself!
=======================

Creating test databases.
------------------------

There are two tags that have django models and migrations setup:
``pure_postgres`` and ``postgis``. Checkout tag needed before running
migrations or debugging with shell.

#.
   Create user and postgres databases with

   .. code-block:: shell

      ./initdb.sh create

   Login to ``test_postgis`` database as superuser and run

   .. code-block:: sql

      CREATE EXTENSION postgis;

#.
   Run migrations for pure_postgres database:

   .. code-block:: shell

      python manage.py migrate --settings=server.settings.pure_postgres

   Run migrations for postgis database:

   .. code-block:: shell

      python manage.py migrate --settings=server.settings.postgis

#.
   Load test data.

   Test data being used for these test are ``RU`` data from `<geonames http://download.geonames.org/export/dump/>`_
   that contains 361k points for Russia. You can use other databases, however specific file preparation
   is needed for importing this data (if you follow this steps, at least. Note also that
   postgres 12 not supported in pgloader < 3.6.1 if you want to use it instead.

   #.
      Preparing pure_postgres data:

      First you need to download above mentioned data and unpack it to ``RU.txt`` somewhere.
      After that, in the same folder run:

    .. code-block:: shell

      awk -F "\t" '{print $2"\t"$3"\t"$3"\t"$6", "$5;}'  RU.txt > RU_postgres.txt

      For postgis data run:

    .. code-block:: shell

      awk -F "\t" '{print $2"\t"$3"\t"$3"\t"$6"\t"$5;}'  RU.txt > RU_posgis.txt

   #.
      Importing data.

      The easiest way is to use ``pgadmin4``. Import ``RU_postgres.txt`` into
      ``test_pure_postgres`` database, ``places_place`` model, specifying tab as a delimeter
      and dropping out ``id`` column since it's auto generated.

      Import ``RU_postgis.txt`` into ``test_postgis`` database, ``places_place`` column
      as described above.

#.
   Testing it's working.

   You can run development server to see if everything is fine:

   .. code-block:: bash

      python manage.py runserver_plus --settings=server.settings.pure_postgres

   Specify ``postgis`` settings file to run development server with PostGIS setup.


#.
   Generated queries:

   For ``pure_postgres`` query

   .. code-block:: python

      Place.objects.filter(coord__contained_in=((37.759, 55.792), (37.487, 55.716))).all()

   Generates following SQL:

   .. code-block:: sql

      SELECT "places_place"."id", "places_place"."title", "places_place"."description_short", "places_place"."description_long", "places_place"."coord"
      FROM "places_place"
      WHERE "places_place"."coord" <@ box '(37.759, 55.792), (37.487, 55.716)'

   Executing this query yields 327 results.

   There are several test queries available in ``test_postgres.rst``
   and ``test_postgis.rst`` files.

#.
   Running tests.

   Test sql files are located in ``test_sql/`` and named after number of rows
   they return. To run query you can use something like:

   .. code-block:: shell

      psql test_pure_postgres -U postgres -f test_sql/5424_postgres.sql

   That will output EXPLAIN ANALYZE results.

   To run query without caching you have to clear caches before each query:

   .. code-block:: shell

      ./drop_caches.sh

.. _Contact me: mailto:aleert@yandex.ru
