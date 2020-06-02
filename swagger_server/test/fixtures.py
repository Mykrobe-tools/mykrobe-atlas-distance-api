from contextlib import contextmanager

from swagger_server.databases.neo4j import Neo4jDatabase


@contextmanager
def managed_db():
    db = Neo4jDatabase()

    try:
        yield db
    finally:
        db.truncate()
