#!/usr/bin/env bash

mkdir -p data/databases
chmod 777 data data/databases

docker run --rm -it -p 8080:8080 -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=none -v $(pwd)/data:/data --name dist dist
