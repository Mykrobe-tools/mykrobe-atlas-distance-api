import logging

import connexion
from flask import g
from pytest import fixture

from swagger_server.encoder import JSONEncoder
from swagger_server.schemas.neo4j import Neo4jSchema


@fixture
def db(db):
    Neo4jSchema.apply(db)

    try:
        yield db
    finally:
        Neo4jSchema.unapply(db)


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
