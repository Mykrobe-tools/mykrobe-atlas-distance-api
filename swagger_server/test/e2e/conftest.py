import logging

import connexion
from pytest import fixture

from swagger_server.encoder import JSONEncoder


@fixture
def app():
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = connexion.App(__name__, specification_dir='../../swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml')

    with app.app.app_context():
        yield app.app


@fixture
def client(app):
    with app.test_client() as client:
        yield client
