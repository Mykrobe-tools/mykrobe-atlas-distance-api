import logging

import connexion
from flask_testing import TestCase

from swagger_server.encoder import JSONEncoder


class BaseTestCase(TestCase):

    def create_app(self):
        # TODO: Create and use a different database once we can upgrade to Neo4j 4.0
        # https://neo4j.com/developer/manage-multiple-databases/

        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/', options={'swagger_ui': False})
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        return app.app
