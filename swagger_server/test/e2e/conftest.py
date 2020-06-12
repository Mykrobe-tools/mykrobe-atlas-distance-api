import logging

import connexion
from pytest import fixture

from swagger_server.encoder import JSONEncoder
from swagger_server.repositories import Neo4jRepository


@fixture
def db():
    db = Neo4jRepository()
    yield db
    db.truncate()


@fixture
def app():
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = connexion.App(__name__, specification_dir='../../swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml')
    return app.app


@fixture
def client(app):
    with app.test_client() as client:
        yield client
