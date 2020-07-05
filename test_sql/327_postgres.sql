EXPLAIN (BUFFERS,
         ANALYZE,
         VERBOSE)
SELECT "places_place"."id",
       "places_place"."title",
       "places_place"."description_short",
       "places_place"."description_long",
       "places_place"."coord"
FROM "places_place"
WHERE "places_place"."coord" <@ BOX '(37.759, 55.792), (37.487, 55.716)'
