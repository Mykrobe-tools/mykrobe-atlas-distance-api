#!/usr/bin/env bash

docker run --rm --name test_neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=none neo4j