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
