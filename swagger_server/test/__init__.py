import logging

import connexion
from flask_testing import TestCase

from swagger_server.encoder import JSONEncoder
from swagger_server.helpers import db


class BaseTestCase(TestCase):

    def create_app(self):
        db.URI = "bolt://localhost:7687"
        db.ENCRYPTED = False
        # NOTE: Creating new databases is only possible in Neo4j Enterprise
        # If using Enterprise edition, we could create a separated db here

        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/', options={'swagger_ui': False})
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        return app.app

        # TODO: Find out how to terminate db at the end of test run
