#!/bin/bash -eu

DIR="/data/databases/neo4j"

if [ ! -d "$DIR" ]
then
    neo4j-admin load --from=/backups/init.db.bak --database=neo4j
fi

exec "$@"
