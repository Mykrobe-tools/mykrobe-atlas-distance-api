from pytest import fixture

from swagger_server.databases.neo4j import Neo4jDatabase


@fixture
def db():
    db = Neo4jDatabase()

    try:
        yield db
    finally:
        db.truncate()
