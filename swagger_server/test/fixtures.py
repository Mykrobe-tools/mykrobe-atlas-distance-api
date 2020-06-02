from contextlib import contextmanager

from swagger_server.databases.neo4j import Neo4JDatabase


@contextmanager
def managed_db():
    db = Neo4JDatabase()
    db.apply_schema()

    yield db

    db.truncate()
