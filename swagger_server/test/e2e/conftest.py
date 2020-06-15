import logging

import connexion
from hypothesis import settings
from pytest import fixture

from swagger_server import registry
from swagger_server.encoder import JSONEncoder
from swagger_server.repositories import Neo4jRepository


@fixture
def db():
    db = Neo4jRepository()
    yield db
    db.truncate()


@fixture
def app(db):
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = connexion.App(__name__, specification_dir='../../swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml')

    with app.app.app_context():
        registry.register('db', db)
        yield app.app


@fixture
def client(app):
    with app.test_client() as client:
        yield client


settings.register_profile('e2e', deadline=None)
settings.load_profile('e2e')
