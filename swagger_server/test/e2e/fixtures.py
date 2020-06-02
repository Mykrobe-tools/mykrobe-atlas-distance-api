from contextlib import contextmanager

from swagger_server.schemas.neo4j import Neo4jSchema
from swagger_server.test.fixtures import managed_db


@contextmanager
def schematised_db():
    with managed_db() as db:
        Neo4jSchema.apply(db)

        try:
            yield db
        finally:
            Neo4jSchema.unapply(db)
