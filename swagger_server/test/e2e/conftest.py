import logging

import connexion
import py2neo
from flask import g
from pytest import fixture

from swagger_server.encoder import JSONEncoder


@fixture
def db():
    db = py2neo.Graph()
    yield db
    db.delete_all()


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
