#!/usr/bin/env bash

mkdir -p data/databases data/transactions
chmod -Rf 777 data || : # on subsequent runs the directory is owned by neo4j's user so this returns error. We ignore that.

docker run --rm -it -p 8080:8080 -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=none -v $(pwd)/data:/data --name dist dist
