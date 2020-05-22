import logging

import connexion
from flask_testing import TestCase
from hypothesis.strategies import register_type_strategy

from swagger_server.encoder import JSONEncoder
from swagger_server.models import Sample
from swagger_server.test.strategies import samples


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        return app.app


register_type_strategy(Sample, samples())