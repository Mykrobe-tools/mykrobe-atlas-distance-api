from pytest import fixture

from swagger_server.adapters.databases.neo4j import Neo4jDatabase


@fixture
def db():
    db = Neo4jDatabase('bolt://localhost:7687', secured=False)

    try:
        yield db
    finally:
        db.truncate()
