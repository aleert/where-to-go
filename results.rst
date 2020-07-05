========
Postgres
========

327 rows returned
=================

Query
^^^^^

.. code-block:: sql

EXPLAIN (BUFFERS ANALYZE VERBOSE)
SELECT "places_place"."id",
       "places_place"."title",
       "places_place"."description_short",
       "places_place"."description_long",
       "places_place"."coord"
FROM "places_place"
WHERE "places_place"."coord" <@ BOX '(37.759, 55.792), (37.487, 55.716)'

Results
^^^^^^^

Without caching:

.. code-block::

 Bitmap Heap Scan on public.places_place  (cost=19.08..1104.24 rows=361 width=59) (actual time=454.380..1256.090 rows=327 loops=1)
  Output: id, title, description_short, description_long, coord
  Recheck Cond: (places_place.coord <@ '(37.759,55.792),(37.487,55.716)'::box)
  Heap Blocks: exact=80
  Buffers: shared read=87
  ->  Bitmap Index Scan on places_plac_coord_d56830_gist  (cost=0.00..18.99 rows=361 width=0) (actual time=439.986..439.986 rows=327 loops=1)
        Index Cond: (places_place.coord <@ '(37.759,55.792),(37.487,55.716)'::box)
        Buffers: shared read=7
 Planning Time: 252.446 ms
 Execution Time: 274.217 ms

 Planning Time: 132.997 ms
 Execution Time: 267.627 ms

 Planning Time: 350.023 ms
 Execution Time: 347.576 ms

 Planning Time: 283.920 ms
 Execution Time: 454.597 ms

 Planning Time: 264.969 ms
 Execution Time: 278.429 ms


With caching:

.. code-block::

 Bitmap Heap Scan on public.places_place  (cost=19.08..1104.24 rows=361 width=59) (actual time=0.178..0.551 rows=327 loops=1)
   Output: id, title, description_short, description_long, coord
   Recheck Cond: (places_place.coord <@ '(37.759,55.792),(37.487,55.716)'::box)
   Heap Blocks: exact=80
   Buffers: shared hit=87
   ->  Bitmap Index Scan on places_plac_coord_d56830_gist  (cost=0.00..18.99 rows=361 width=0) (actual time=0.131..0.131 rows=327 loops=1)
         Index Cond: (places_place.coord <@ '(37.759,55.792),(37.487,55.716)'::box)
         Buffers: shared hit=7
 Planning Time: 1.026 ms
 Execution Time: 0.811 ms

 Planning Time: 0.973 ms
 Execution Time: 0.810 ms

 Planning Time: 0.983 ms
 Execution Time: 0.863 ms

 Planning Time: 0.420 ms
 Execution Time: 0.311 ms

 Planning Time: 0.867 ms
 Execution Time: 0.611 ms

 Planning Time: 0.287 ms
 Execution Time: 0.272 ms

 Planning Time: 0.944 ms
 Execution Time: 0.805 ms



4424 rows returned
==================

Query
^^^^^

EXPLAIN (BUFFERS,
         ANALYZE,
         VERBOSE)
SELECT "places_place"."id",
       "places_place"."title",
       "places_place"."description_short",
       "places_place"."description_long",
       "places_place"."coord"
FROM "places_place"
WHERE "places_place"."coord" <@ BOX '(67.759, 63.792), (73.487, 50.716)'

Results
^^^^^^^

Without caching:

.. code-block::

 Bitmap Heap Scan on public.places_place  (cost=19.08..1104.24 rows=361 width=59) (actual time=243.050..394.798 rows=5424 loops=1)
   Output: id, title, description_short, description_long, coord
   Recheck Cond: (places_place.coord <@ '(73.487,63.792),(67.759,50.716)'::box)
   Heap Blocks: exact=417
   Buffers: shared read=486
   ->  Bitmap Index Scan on places_plac_coord_d56830_gist  (cost=0.00..18.99 rows=361 width=0) (actual time=231.584..231.584 rows=5424 loops=1)
         Index Cond: (places_place.coord <@ '(73.487,63.792),(67.759,50.716)'::box)
         Buffers: shared read=69
 Planning Time: 298.707 ms
 Execution Time: 396.525 ms

 Bitmap Heap Scan on public.places_place  (cost=19.08..1104.24 rows=361 width=59) (actual time=248.183..388.794 rows=5424 loops=1)
   Output: id, title, description_short, description_long, coord
   Recheck Cond: (places_place.coord <@ '(73.487,63.792),(67.759,50.716)'::box)
   Heap Blocks: exact=417
   Buffers: shared read=486
   ->  Bitmap Index Scan on places_plac_coord_d56830_gist  (cost=0.00..18.99 rows=361 width=0) (actual time=237.251..237.251 rows=5424 loops=1)
         Index Cond: (places_place.coord <@ '(73.487,63.792),(67.759,50.716)'::box)
         Buffers: shared read=69
 Planning Time: 180.963 ms
 Execution Time: 393.134 ms

 Planning Time: 210.213 ms
 Execution Time: 396.815 ms

 Planning Time: 125.876 ms
 Execution Time: 393.225 ms

 Planning Time: 243.391 ms
 Execution Time: 462.749 ms

With caching:

.. code-block::

 Bitmap Heap Scan on public.places_place  (cost=19.08..1104.24 rows=361 width=59) (actual time=1.055..2.629 rows=5424 loops=1)
   Output: id, title, description_short, description_long, coord
   Recheck Cond: (places_place.coord <@ '(73.487,63.792),(67.759,50.716)'::box)
   Heap Blocks: exact=417
   Buffers: shared hit=486
   ->  Bitmap Index Scan on places_plac_coord_d56830_gist  (cost=0.00..18.99 rows=361 width=0) (actual time=0.958..0.958 rows=5424 loops=1)
         Index Cond: (places_place.coord <@ '(73.487,63.792),(67.759,50.716)'::box)
         Buffers: shared hit=69
 Planning Time: 0.523 ms
 Execution Time: 3.055 ms

 Planning Time: 0.302 ms
 Execution Time: 1.897 ms

 Planning Time: 0.333 ms
 Execution Time: 2.206 ms

 Planning Time: 0.287 ms
 Execution Time: 1.924 ms

 Planning Time: 0.285 ms
 Execution Time: 1.939 ms

 Planning Time: 0.348 ms
 Execution Time: 2.172 ms


=====================
Postgres with postgis
=====================

327 rows returned
=================

Query
^^^^^

.. code-block:: sql

   EXPLAIN (BUFFERS, ANALYZE, VERBOSE) SELECT "places_place"."id",
          "places_place"."title",
          "places_place"."description_short",
          "places_place"."description_long",
          "places_place"."coord"::BYTEA
   FROM "places_place"
   WHERE "places_place"."coord" @ ST_GeomFromEWKB('\001\003\000\000 \346\020\000\000\001\000\000\000\005\000\000\000u\223\030\004V\276B@\317\367S\343\245\333K@u\223\030\004V\276B@L7\211A`\345K@\376\324x\351&\341B@L7\211A`\345K@\376\324x\351&\341B@\317\367S\343\245\333K@u\223\030\004V\276B@\317\367S\343\245\333K@'::BYTEA)

Query with coveredby
^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   EXPLAIN (BUFFERS, ANALYZE, VERBOSE) SELECT "places_place"."id",
          "places_place"."title",
          "places_place"."description_short",
          "places_place"."description_long",
          "places_place"."coord"::BYTEA
   FROM "places_place"
   WHERE ST_CoveredBy("places_place"."coord", ST_GeomFromEWKB('\001\003\000\000 \346\020\000\000\001\000\000\000\005\000\000\000u\223\030\004V\276B@\317\367S\343\245\333K@u\223\030\004V\276B@L7\211A`\345K@\376\324x\351&\341B@L7\211A`\345K@\376\324x\351&\341B@\317\367S\343\245\333K@u\223\030\004V\276B@\317\367S\343\245\333K@'::BYTEA))

Results
^^^^^^^

Without caching:
~~~~~~~~~~~~~~~~

.. code-block::

 Bitmap Heap Scan on public.places_place  (cost=15.08..1215.78 rows=361 width=75) (actual time=57.840..222.850 rows=327 loops=1)
   Output: id, title, description_short, description_long, (coord)::bytea
   Recheck Cond: (places_place.coord @ '0103000020E610000001000000050000007593180456BE4240CFF753E3A5DB4B407593180456BE42404C37894160E54B40FED478E926E142404C37894160E54B40FED478E926E14240CFF753E3A5DB4B407593180456BE4240CFF753E3A5DB4B40'::geometry)
   Heap Blocks: exact=83
   Buffers: shared read=90
   ->  Bitmap Index Scan on places_place_coord_id  (cost=0.00..14.99 rows=361 width=0) (actual time=54.031..54.031 rows=327 loops=1)
         Index Cond: (places_place.coord @ '0103000020E610000001000000050000007593180456BE4240CFF753E3A5DB4B407593180456BE42404C37894160E54B40FED478E926E142404C37894160E54B40FED478E926E14240CFF753E3A5DB4B407593180456BE4240CFF753E3A5DB4B40'::geometry)
         Buffers: shared read=7
 Planning Time: 1070.382 ms
 Execution Time: 224.427 ms

 Planning Time: 1078.605 ms
 Execution Time: 406.719 ms

 Planning Time: 1198.153 ms
 Execution Time: 336.346 ms

 Planning Time: 1168.908 ms
 Execution Time: 320.970 ms

 Planning Time: 1172.228 ms
 Execution Time: 363.152 ms


With caching:
~~~~~~~~~~~~~

.. code-block::

 Bitmap Heap Scan on public.places_place  (cost=15.08..1215.78 rows=361 width=75) (actual time=0.139..0.413 rows=327 loops=1)
   Output: id, title, description_short, description_long, (coord)::bytea
   Recheck Cond: (places_place.coord @ '0103000020E610000001000000050000007593180456BE4240CFF753E3A5DB4B407593180456BE42404C37894160E54B40FED478E926E142404C37894160E54B40FED478E926E14240CFF753E3A5DB4B407593180456BE4240CFF753E3A5DB4B40'::geometry)
   Heap Blocks: exact=83
   Buffers: shared hit=90
   ->  Bitmap Index Scan on places_place_coord_id  (cost=0.00..14.99 rows=361 width=0) (actual time=0.123..0.123 rows=327 loops=1)
         Index Cond: (places_place.coord @ '0103000020E610000001000000050000007593180456BE4240CFF753E3A5DB4B407593180456BE42404C37894160E54B40FED478E926E142404C37894160E54B40FED478E926E14240CFF753E3A5DB4B407593180456BE4240CFF753E3A5DB4B40'::geometry)
         Buffers: shared hit=7
 Planning Time: 67.729 ms
 Execution Time: 0.562 ms

 Planning Time: 27.447 ms
 Execution Time: 0.566 ms

 Planning Time: 56.419 ms
 Execution Time: 0.558 ms

 Planning Time: 46.337 ms
 Execution Time: 0.761 ms

 Planning Time: 25.865 ms
 Execution Time: 0.579 ms

 Planning Time: 44.303 ms
 Execution Time: 0.574 ms

 Planning Time: 27.488 ms
 Execution Time: 0.602 ms

 Planning Time: 51.957 ms
 Execution Time: 0.574 ms

Coveredby version with caching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

 Bitmap Heap Scan on public.places_place  (cost=15.00..10163.30 rows=55 width=75) (actual time=0.114..0.489 rows=327 loops=1)
   Output: id, title, description_short, description_long, (coord)::bytea
   Filter: st_coveredby(places_place.coord, '0103000020E610000001000000050000007593180456BE4240CFF753E3A5DB4B407593180456BE42404C37894160E54B40FED478E926E142404C37894160E54B40FED478E926E14240CFF753E3A5DB4B407593180456BE4240CFF753E3A5DB4B40'::geometry)
   Heap Blocks: exact=83
   Buffers: shared hit=90
   ->  Bitmap Index Scan on places_place_coord_id  (cost=0.00..14.99 rows=361 width=0) (actual time=0.095..0.096 rows=327 loops=1)
         Index Cond: (places_place.coord @ '0103000020E610000001000000050000007593180456BE4240CFF753E3A5DB4B407593180456BE42404C37894160E54B40FED478E926E142404C37894160E54B40FED478E926E14240CFF753E3A5DB4B407593180456BE4240CFF753E3A5DB4B40'::geometry)
         Buffers: shared hit=7
 Planning Time: 25.323 ms
 Execution Time: 0.634 ms

 Planning Time: 46.844 ms
 Execution Time: 0.650 ms

 Planning Time: 32.106 ms
 Execution Time: 0.642 ms

 Planning Time: 24.559 ms
 Execution Time: 0.615 ms

 Planning Time: 36.410 ms
 Execution Time: 0.635 ms

Coveredby version without caching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

 Bitmap Heap Scan on public.places_place  (cost=15.00..10163.30 rows=55 width=75) (actual time=95.768..293.553 rows=327 loops=1)
   Output: id, title, description_short, description_long, (coord)::bytea
   Filter: st_coveredby(places_place.coord, '0103000020E610000001000000050000007593180456BE4240CFF753E3A5DB4B407593180456BE42404C37894160E54B40FED478E926E142404C37894160E54B40FED478E926E14240CFF753E3A5DB4B407593180456BE4240CFF753E3A5DB4B40'::geometry)
   Heap Blocks: exact=83
   Buffers: shared read=90
   ->  Bitmap Index Scan on places_place_coord_id  (cost=0.00..14.99 rows=361 width=0) (actual time=91.995..91.995 rows=327 loops=1)
         Index Cond: (places_place.coord @ '0103000020E610000001000000050000007593180456BE4240CFF753E3A5DB4B407593180456BE42404C37894160E54B40FED478E926E142404C37894160E54B40FED478E926E14240CFF753E3A5DB4B407593180456BE4240CFF753E3A5DB4B40'::geometry)
         Buffers: shared read=7
 Planning Time: 1235.384 ms
 Execution Time: 347.613 ms

 Planning Time: 1483.402 ms
 Execution Time: 248.754 ms

 Planning Time: 1180.108 ms
 Execution Time: 262.669 ms

 Planning Time: 1503.570 ms
 Execution Time: 281.428 ms

 Planning Time: 1649.297 ms
 Execution Time: 292.859 ms


5424 rows returned
=================

Query
^^^^^

.. code-block:: sql

   EXPLAIN (BUFFERS,
            ANALYZE,
            VERBOSE)
   SELECT "places_place"."id",
          "places_place"."title",
          "places_place"."description_short",
          "places_place"."description_long",
          "places_place"."coord"::BYTEA
   FROM "places_place"
   WHERE "places_place"."coord" @ ST_GeomFromEWKB('\001\003\000\000 \346\020\000\000\001\000\000\000\005\000\000\000\177j\274t\223\360P@\317\367S\343\245[I@\177j\274t\223\360P@L7\211A`\345O@\272I\014\002+_R@L7\211A`\345O@\272I\014\002+_R@\317\367S\343\245[I@\177j\274t\223\360P@\317\367S\343\245[I@'::BYTEA)

Query with coveredby
^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   SELECT "places_place"."id",
          "places_place"."title",
          "places_place"."description_short",
          "places_place"."description_long",
          "places_place"."coord"::BYTEA
   FROM "places_place"
   WHERE ST_CoveredBy("places_place"."coord", ST_GeomFromEWKB('\001\003\000\000 \346\020\000\000\001\000\000\000\005\000\000\000\177j\274t\223\360P@\317\367S\343\245[I@\177j\274t\223\360P@L7\211A`\345O@\272I\014\002+_R@L7\211A`\345O@\272I\014\002+_R@\317\367S\343\245[I@\177j\274t\223\360P@\317\367S\343\245[I@'::BYTEA))

Results
^^^^^^^

Without caching:
~~~~~~~~~~~~~~~~

.. code-block::

 Bitmap Heap Scan on public.places_place  (cost=15.08..1215.78 rows=361 width=75) (actual time=261.174..439.990 rows=5424 loops=1)
   Output: id, title, description_short, description_long, (coord)::bytea
   Recheck Cond: (places_place.coord @ '0103000020E610000001000000050000007F6ABC7493F05040CFF753E3A55B49407F6ABC7493F050404C37894160E54F40BA490C022B5F52404C37894160E54F40BA490C022B5F5240CFF753E3A55B49407F6ABC7493F05040CFF753E3A55B4940'::geometry)
   Heap Blocks: exact=462
   Buffers: shared read=519
   ->  Bitmap Index Scan on places_place_coord_id  (cost=0.00..14.99 rows=361 width=0) (actual time=251.769..251.770 rows=5424 loops=1)
         Index Cond: (places_place.coord @ '0103000020E610000001000000050000007F6ABC7493F05040CFF753E3A55B49407F6ABC7493F050404C37894160E54F40BA490C022B5F52404C37894160E54F40BA490C022B5F5240CFF753E3A55B49407F6ABC7493F05040CFF753E3A55B4940'::geometry)
         Buffers: shared read=57
 Planning Time: 1221.578 ms
 Execution Time: 442.737 ms

 Planning Time: 1179.436 ms
 Execution Time: 395.899 ms

 Planning Time: 1121.350 ms
 Execution Time: 366.098 ms

 Planning Time: 1077.512 ms
 Execution Time: 388.103 ms

 Planning Time: 1330.316 ms
 Execution Time: 333.107 ms


With caching
~~~~~~~~~~~~

 Bitmap Heap Scan on public.places_place  (cost=15.08..1215.78 rows=361 width=75) (actual time=0.792..3.326 rows=5424 loops=1)
   Output: id, title, description_short, description_long, (coord)::bytea
   Recheck Cond: (places_place.coord @ '0103000020E610000001000000050000007F6ABC7493F05040CFF753E3A55B49407F6ABC7493F050404C37894160E54F40BA490C022B5F52404C37894160E54F40BA490C022B5F5240CFF753E3A55B49407F6ABC7493F05040CFF753E3A55B4940'::geometry)
   Heap Blocks: exact=462
   Buffers: shared hit=519
   ->  Bitmap Index Scan on places_place_coord_id  (cost=0.00..14.99 rows=361 width=0) (actual time=0.727..0.727 rows=5424 loops=1)
         Index Cond: (places_place.coord @ '0103000020E610000001000000050000007F6ABC7493F05040CFF753E3A55B49407F6ABC7493F050404C37894160E54F40BA490C022B5F52404C37894160E54F40BA490C022B5F5240CFF753E3A55B49407F6ABC7493F05040CFF753E3A55B4940'::geometry)
         Buffers: shared hit=57
 Planning Time: 25.639 ms
 Execution Time: 3.663 ms

 Planning Time: 51.752 ms
 Execution Time: 3.892 ms

 Planning Time: 25.728 ms
 Execution Time: 3.748 ms

 Planning Time: 48.787 ms
 Execution Time: 4.234 ms

 Planning Time: 35.484 ms
 Execution Time: 3.800 ms

 Planning Time: 46.623 ms
 Execution Time: 3.945 ms

 Planning Time: 39.173 ms
 Execution Time: 4.049 ms

 Planning Time: 24.765 ms
 Execution Time: 3.836 ms


Coveredby version without caching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Bitmap Heap Scan on public.places_place  (cost=16.34..11497.88 rows=5388 width=75) (actual time=154.688..344.583 rows=5424 loops=1)
   Output: id, title, description_short, description_long, (coord)::bytea
   Filter: st_coveredby(places_place.coord, '0103000020E610000001000000050000007F6ABC7493F05040CFF753E3A55B49407F6ABC7493F050404C37894160E54F40BA490C022B5F52404C37894160E54F40BA490C022B5F5240CFF753E3A55B49407F6ABC7493F05040CFF753E3A55B4940'::geometry)
   Heap Blocks: exact=462
   Buffers: shared read=519
   ->  Bitmap Index Scan on places_place_coord_id  (cost=0.00..14.99 rows=361 width=0) (actual time=145.246..145.246 rows=5424 loops=1)
         Index Cond: (places_place.coord @ '0103000020E610000001000000050000007F6ABC7493F05040CFF753E3A55B49407F6ABC7493F050404C37894160E54F40BA490C022B5F52404C37894160E54F40BA490C022B5F5240CFF753E3A55B49407F6ABC7493F05040CFF753E3A55B4940'::geometry)
         Buffers: shared read=57
 Planning Time: 1384.923 ms
 Execution Time: 432.322 ms

 Planning Time: 1251.127 ms
 Execution Time: 465.235 ms

 Planning Time: 1272.686 ms
 Execution Time: 465.410 ms

 Planning Time: 1295.142 ms
 Execution Time: 388.312 ms

 Planning Time: 1373.709 ms
 Execution Time: 630.103 ms


Coveredby version with caching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Bitmap Heap Scan on public.places_place  (cost=16.34..11497.88 rows=5388 width=75) (actual time=0.904..6.547 rows=5424 loops=1)
   Output: id, title, description_short, description_long, (coord)::bytea
   Filter: st_coveredby(places_place.coord, '0103000020E610000001000000050000007F6ABC7493F05040CFF753E3A55B49407F6ABC7493F050404C37894160E54F40BA490C022B5F52404C37894160E54F40BA490C022B5F5240CFF753E3A55B49407F6ABC7493F05040CFF753E3A55B4940'::geometry)
   Heap Blocks: exact=462
   Buffers: shared hit=519
   ->  Bitmap Index Scan on places_place_coord_id  (cost=0.00..14.99 rows=361 width=0) (actual time=0.823..0.824 rows=5424 loops=1)
         Index Cond: (places_place.coord @ '0103000020E610000001000000050000007F6ABC7493F05040CFF753E3A55B49407F6ABC7493F050404C37894160E54F40BA490C022B5F52404C37894160E54F40BA490C022B5F5240CFF753E3A55B49407F6ABC7493F05040CFF753E3A55B4940'::geometry)
         Buffers: shared hit=57
 Planning Time: 47.672 ms
 Execution Time: 6.904 ms

 Planning Time: 25.138 ms
 Execution Time: 6.701 ms

 Planning Time: 52.881 ms
 Execution Time: 6.826 ms

 Planning Time: 25.097 ms
 Execution Time: 6.498 ms

 Planning Time: 25.300 ms
 Execution Time: 6.660 ms

 Planning Time: 25.357 ms
 Execution Time: 6.611 ms

 Planning Time: 35.038 ms
 Execution Time: 7.061 ms

 Planning Time: 34.802 ms
 Execution Time: 6.646 ms


