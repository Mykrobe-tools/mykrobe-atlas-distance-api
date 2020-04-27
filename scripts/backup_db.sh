#!/usr/bin/env bash

docker exec -ti dist supervisorctl stop neo4j
docker exec -ti dist neo4j-admin dump --to=/data/init.db.bak --database=graph.db
docker exec -ti dist supervisorctl start neo4j

cp ./data/init.db.bak ./backups/
