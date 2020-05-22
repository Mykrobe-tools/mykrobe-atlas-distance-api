from swagger_server.drivers import Neo4jDriver
from swagger_server.drivers.exceptions import SchemaExisted
from swagger_server.migrations.neo4j import NEO4J_MIGRATIONS


def migrate():
    for forward, _ in NEO4J_MIGRATIONS:
        try:
            Neo4jDriver.get().modify_schema(forward)
        except SchemaExisted:
            pass