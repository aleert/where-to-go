#!/usr/bin/env sh


if [ "$1" = "create" ]; then
    psql -U postgres -f ./sql/create_database.sql
elif [ "$1" = "drop" ]; then
    psql -U postgres -f ./sql/drop_database.sql
else
    echo "Specify either \"create\" or \"drop\" to create or drop database."
fi
