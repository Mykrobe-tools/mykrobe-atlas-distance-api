import logging

import connexion
from flask_testing import TestCase
from hypothesis.strategies import register_type_strategy

from swagger_server.encoder import JSONEncoder
from swagger_server.helpers import db
from swagger_server.migrate import migrate
from swagger_server.models import Neighbour
from swagger_server.test.strategies import neighbours


class BaseTestCase(TestCase):

    docker_container_name = 'test_neo4j'
    app = None

    @classmethod
    def setUpClass(cls):
        db.URI = "bolt://localhost:7687"
        db.ENCRYPTED = False
        db.Neo4jDatabase.get().connect()
        migrate(db.Neo4jDatabase.get().driver)

        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/', options={'swagger_ui': False})
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        cls.app = app.app

    @classmethod
    def tearDownClass(cls):
        db.Neo4jDatabase.get().query('MATCH (n) DETACH DELETE n', write=True)
        db.Neo4jDatabase.get().close()

    def create_app(self):
        return self.app


register_type_strategy(Neighbour, neighbours())
