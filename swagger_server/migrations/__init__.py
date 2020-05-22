from swagger_server.drivers import Neo4jDriver
from swagger_server.drivers.exceptions import SchemaExistedError
from swagger_server.migrations.neo4j import NEO4J_MIGRATIONS


def migrate():
    for forward, _ in NEO4J_MIGRATIONS:
        try:
            Neo4jDriver.get().execute(forward)
        except SchemaExistedError:
            pass
