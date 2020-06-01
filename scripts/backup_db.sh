#!/usr/bin/env bash

docker exec -ti dist supervisorctl stop neo4j
docker exec -ti dist neo4j-admin dump --to=/backups/init.db.bak --database=neo4j
docker exec -ti dist supervisorctl start neo4j
