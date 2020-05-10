import logging
import os
import subprocess
from time import sleep

import connexion
from flask_testing import TestCase

from swagger_server.encoder import JSONEncoder
from swagger_server.helpers import db


class BaseTestCase(TestCase):

    docker_container_name = 'test_neo4j'

    @classmethod
    def setUpClass(cls):
        db.URI = "bolt://localhost:7687"
        db.ENCRYPTED = False

    @classmethod
    def tearDownClass(cls):
        db.Neo4jDatabase.get().query('MATCH (n) DETACH DELETE n')

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/', options={'swagger_ui': False})
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        return app.app
