EXPLAIN (BUFFERS,
         ANALYZE,
         VERBOSE)
SELECT "places_place"."id",
       "places_place"."title",
       "places_place"."description_short",
       "places_place"."description_long",
       "places_place"."coord"::BYTEA
FROM "places_place"
WHERE "places_place"."coord" @ ST_GeomFromEWKB('\001\003\000\000 \346\020\000\000\001\000\000\000\005\000\000\000u\223\030\004V\276B@\317\367S\343\245\333K@u\223\030\004V\276B@L7\211A`\345K@\376\324x\351&\341B@L7\211A`\345K@\376\324x\351&\341B@\317\367S\343\245\333K@u\223\030\004V\276B@\317\367S\343\245\333K@'::BYTEA)
