import logging
import os

import connexion
from flask import g
from pytest import fixture

from swagger_server.adapters.graph.in_memory import InMemoryGraph
from swagger_server.adapters.graph.persistent import PersistentGraph
from swagger_server.encoder import JSONEncoder


@fixture
def db():
    if os.environ.get('DB') == 'persistent':
        return PersistentGraph()
    return InMemoryGraph()


@fixture
def app(db):
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = connexion.App(__name__, specification_dir='../../swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml')

    with app.app.app_context():
        g.db = db
        yield app.app


@fixture
def client(app):
    with app.test_client() as client:
        yield client
