#!/usr/bin/env bash

docker exec -ti dist bash -c "rm -rf /data/databases/* && rm -rf /data/transactions/*"
docker exec -ti dist supervisorctl restart neo4j
sleep 5
docker exec -ti dist python3 -m swagger_server.migrate
docker exec -ti dist python3 -m swagger_server.initdb
