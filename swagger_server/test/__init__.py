import logging
import unittest

import connexion
from flask_testing import TestCase
from hypothesis.strategies import register_type_strategy

from swagger_server.encoder import JSONEncoder
from swagger_server.migrations import migrate
from swagger_server.models import Sample
from swagger_server.test.strategies import samples


class DBTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        migrate()


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        return app.app


register_type_strategy(Sample, samples())