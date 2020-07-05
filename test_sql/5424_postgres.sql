EXPLAIN (BUFFERS, ANALYZE, VERBOSE) SELECT "places_place"."id", "places_place"."title", "places_place"."description_short", "places_place"."description_long", "places_place"."coord"
FROM "places_place"
WHERE "places_place"."coord" <@ box '(67.759, 63.792), (73.487, 50.716)'
