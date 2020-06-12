#!/usr/bin/env bash

USER_ID=$(id -u $(whoami))
FILE_PATH="/backups/init.db.bak"

rm backups/*

docker exec -ti dist supervisorctl stop neo4j
docker exec -ti --user=root -e FILE_PATH=$FILE_PATH dist neo4j-admin dump --to=$FILE_PATH --database=neo4j
docker exec -ti dist supervisorctl start neo4j

docker exec -ti --user=root -e USER_ID=$USER_ID -e FILE_PATH=$FILE_PATH dist chown $USER_ID $FILE_PATH
