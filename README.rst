=============================
Stress testing with PostGIS
=============================

This branch intended for comparing performance for query that select
Place models based on their coordinates being contained in some geometric box.
Contained box is defined by two opposite angles.

**TL;DR**

   It runs faster if we implement custom django wrappers for native postgresql
   geometry types. Mainly because planning with postgis much more expensive.


Setup
=====

There are two setups to compare:

#.
   Regular postgres with custom field on django side, interfacing postgres
   ``point`` field and custom django lookup implementing ``WHERE point (x, y) <@ box (coords)``.

   There's also a ``GistIndex`` created with point field to increase above mentioned
   lookup performance. For further details refer to ``fields.py`` and ``models.PurePostgresPlace``
   in ``places`` app.

   (This setup based on ``progressive-loading`` branch from this repo, clone it if you
   want to explore and see it in action)

#.
   This setup have ``PostGIS`` enabled and utilizes ``GeoDjango`` capabilities.

   If you look at models you'll notice, that there's no index. That's because
   GeoDjango will create gist index automatically, and if we specify it explicitly
   out migrations will fail.

   We use test two different lookup types: one uses ``contained`` django lookup
   and the other uses ``coveredby`` lookup. They both yield the same result.
   Here's django code for them:

   .. code-block:: python

      from django.contrib.gis.geos import Polygon
      p = Polygon.from_bbox((37.487, 55.716, 37.759, 55.792))

      qs = Place.objects.filter(coord__contained=p).all()
      qs2 = Place.objects.filter(coord__coveredby=p).all()

Test data
=========

Test databases use `geonames`_ ``RU`` test data, containing 361+k locations.
Fields missing from geopoints data (short and long description) were generated from names.
Data preparing process described in `preparing test data section`_.

Method
======

SQL requests were generated from django querysets for different bounding boxes,
then they were executed with ``EXPLAIN ANALYZE``. Actual requests can be found
at ``test_sql`` folder. Number in sql file name stands for number of rows returned,
other part of the name describe setup used.

Requests were made both one after another and with cache clear before each request.
Cache clear was done with ``drop_caches.sh``.

Results
=======

.. code-block::

   ╔═══════════════════╦════════════╦═════════════════════════════════╦═════════════════════════════════╗
   ║                   ║            ║          327 rows query         ║         5424 rows query         ║
   ║                   ║            ║         (mean time, ms)         ║         (mean time, ms)         ║
   ║                   ║            ║                                 ║                                 ║
   ╠═══════════════════╬════════════╬══════════╦═══════════╦══════════╬══════════╦═══════════╦══════════╣
   ║                   ║            ║ planning ║ execution ║ total    ║ planning ║ execution ║ total    ║
   ╠═══════════════════╬════════════╬══════════╬═══════════╬══════════╬══════════╬═══════════╬══════════╣
   ║ pure postgres     ║ with cache ║ 0.786    ║ 0.64      ║ 1.426    ║ 0.346    ║ 2.2       ║ 2.546    ║
   ║ (custom django    ╠════════════╬══════════╬═══════════╬══════════╬══════════╬═══════════╬══════════╣
   ║ wrappers)         ║ without    ║ 256.871  ║ 324.489   ║ 581.36   ║ 190.11   ║ 411.48    ║ 601.59   ║
   ║                   ║ cache      ║          ║           ║          ║          ║           ║          ║
   ╠═══════════════════╬════════════╬══════════╬═══════════╬══════════╬══════════╬═══════════╬══════════╣
   ║ postgres with     ║ with cache ║ 43.443   ║ 0.597     ║ 44.04    ║ 37.244   ║ 3.896     ║ 41.14    ║
   ║ postgis           ║            ║          ║           ║          ║          ║           ║          ║
   ║ (contained django ╠════════════╬══════════╬═══════════╬══════════╬══════════╬═══════════╬══════════╣
   ║ query)            ║ without    ║ 1137.655 ║ 330.322   ║ 1467.978 ║ 1186.038 ║ 385.188   ║ 1571.227 ║
   ║                   ║ cache      ║          ║           ║          ║          ║           ║          ║
   ╠═══════════════════╬════════════╬══════════╬═══════════╬══════════╬══════════╬═══════════╬══════════╣
   ║ postgres with     ║ with cache ║ 33.448   ║ 0.635     ║ 34.083   ║ 33.922   ║ 6.738     ║ 40.66    ║
   ║ postgis           ╠════════════╬══════════╬═══════════╬══════════╬══════════╬═══════════╬══════════╣
   ║ (coveredby django ║ without    ║ 1410.352 ║ 286.664   ║ 1697.016 ║ 1315.517 ║ 476.276   ║ 1791.793 ║
   ║ query)            ║ cache      ║          ║           ║          ║          ║           ║          ║
   ╚═══════════════════╩════════════╩══════════╩═══════════╩══════════╩══════════╩═══════════╩══════════╝

As we can see, native solution is faster than PostGis version, mainly because of slow
query planning (while postgis query plans still use same indexes as native version).
Postgis query planning can be for up to 100 times slower than native version when there's some system cache present.
Query execution time do not differ much between versions, which is expected.

You can see some results along with query plans in ``results.rst`` file.


Host machine configuration
==========================

Debian 10 with Postgresql 12 installed, 8gb RAM, Intel Core i5-8250U

This project uses python 3.8.2 with django 3.0.7 and psycopg2 builded with --no-binary option.
Other packages can be viewed in ``requirements/local.txt`` and ``requirements/base.txt``.


I want to do it myself!
=======================

This repo have an environment file to run django locally as well as
script for creating and dropping a databases. You can define your own databases,
just don't forget to change ``.envs/.local/.django/.env`` and database names
in ``server/settings/local.py``.


Creating test databases.
------------------------

First you need to create two databases: ``pure_postgres`` and ``postgis``.
There's a sample sql scripts in ``sql/`` folder, or you can create user
and databases with

.. code-block:: shell

   ./initdb.sh create

After that login to ``test_postgis`` database as superuser and run

.. code-block:: sql

   CREATE EXTENSION postgis;


#.
   There are two tags that have django models and migrations setup:
   ``pure_postgres`` and ``postgis``. Checkout tag needed before running
   migrations or debugging with shell.

#.
   Run migrations for pure_postgres database:

   .. code-block:: shell

      python manage.py migrate --settings=server.settings.pure_postgres

   Run migrations for postgis database:

   .. code-block:: shell

      python manage.py migrate --settings=server.settings.postgis

#.
   Load test data.

   Test data being used for these test are ``RU`` data from `geonames`_
   that contains 361k points for Russia. You can use other databases, however specific file preparation
   is needed for importing this data (if you follow this steps, at least. Note also that
   postgres 12 not supported in pgloader < 3.6.1 if you want to use it instead.

   .. _preparing test data section:

   #.
      Preparing pure_postgres data:

      First you need to download above mentioned data and unpack it to ``RU.txt`` somewhere.
      After that, in the same folder run:

      .. code-block:: shell

         awk -F "\t" '{print $2"\t"$3"\t"$3"\t"$6", "$5;}'  RU.txt > RU_postgres.txt

      For postgis data run:

      .. code-block:: shell

         awk -F "\t" '{print $2"\t"$3"\t"$3"\tSRID=4326;POINT("$6" "$5")";}'  RU.txt > RU_posgis.txt

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

   ``postgis`` version isn't working as for now, as ``places/views.py`` should be
   altered for postgis syntax.


#.
   Generated queries:

   For ``pure_postgres`` query

   .. code-block:: python

      Place.objects.filter(coord__contained_in=((37.759, 55.792), (37.487, 55.716))).all()

   Generates following SQL:

   .. code-block:: sql

      SELECT "places_place"."id",
             "places_place"."title",
             "places_place"."description_short",
             "places_place"."description_long",
             "places_place"."coord"
      FROM "places_place"
      WHERE "places_place"."coord" <@ BOX '(37.759, 55.792), (37.487, 55.716)'

   Executing this query yields 327 results.

   For ``postgis`` we have to do following:

   .. code-block:: python

      from django.contrib.gis.geos import Polygon
      p = Polygon.from_bbox((37.487, 55.716, 37.759, 55.792))

      qs = Place.objects.filter(coord__contained=p).all()

      len(qs)
      327

   That will generate this sql query:

   .. code-block:: sql

      SELECT "places_place"."id",
             "places_place"."title",
             "places_place"."description_short",
             "places_place"."description_long",
             "places_place"."coord"::BYTEA
      FROM "places_place"
      WHERE "places_place"."coord" @ ST_GeomFromEWKB('\001\003\000\000 \346\020\000\000\001\000\000\000\005\000\000\000u\223\030\004V\276B@\317\367S\343\245\333K@u\223\030\004V\276B@L7\211A`\345K@\376\324x\351&\341B@L7\211A`\345K@\376\324x\351&\341B@\317\367S\343\245\333K@u\223\030\004V\276B@\317\367S\343\245\333K@'::BYTEA)

   Note also you can use ``coord__coveredby`` to get the same result. It will yield
   following query:

   .. code-block:: sql

      SELECT "places_place"."id",
             "places_place"."title",
             "places_place"."description_short",
             "places_place"."description_long",
             "places_place"."coord"::BYTEA
      FROM "places_place"
      WHERE ST_CoveredBy("places_place"."coord", ST_GeomFromEWKB('\001\003\000\000 \346\020\000\000\001\000\000\000\005\000\000\000u\223\030\004V\276B@\317\367S\343\245\333K@u\223\030\004V\276B@L7\211A`\345K@\376\324x\351&\341B@L7\211A`\345K@\376\324x\351&\341B@\317\367S\343\245\333K@u\223\030\004V\276B@\317\367S\343\245\333K@'::BYTEA))

#.
   Running SQL tests.

   Test sql files are located in ``test_sql/`` and named after number of rows
   they return. To run query you can use something like:

   .. code-block:: shell

      psql test_pure_postgres -U postgres -f test_sql/5424_postgres.sql

   That will output EXPLAIN ANALYZE results.

   To run query without caching you have to clear caches before each query:

   .. code-block:: shell

      ./drop_caches.sh

`Contact me`_ if you have any questions.

.. _Contact me: mailto:aleert@yandex.ru
.. _geonames: http://download.geonames.org/export/dump/
