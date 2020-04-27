#!/bin/bash -eu

DIR="/data/databases/graph.db"

if [ ! -d "$DIR" ]
then
    neo4j-admin load --from=backups/init.db.bak --database=graph.db
fi

exec "$@"
