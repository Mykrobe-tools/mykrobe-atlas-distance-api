#!/usr/bin/env bash

CONF="$NEO4J_HOME"/conf/neo4j.conf

curl -k -LO https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/graph-data-science/neo4j-graph-data-science-1.1.0-standalone.zip
unzip -d "$NEO4J_HOME"/plugins neo4j-graph-data-science-1.1.0-standalone.zip
sed -i 's/#dbms.security\.procedures\.unrestricted.+/dbms.security.procedures.unrestricted=gds.*/' "$CONF"
sed -i 's/#dbms.security\.procedures\.whitelist.+/dbms.security.procedures.whitelist=gds.*/' "$CONF"
