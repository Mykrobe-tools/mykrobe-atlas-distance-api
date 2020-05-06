import logging
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

        print('creating db')
        subprocess.run(['docker', 'run', '--rm', '-d',
                        '-p', '7474:7474', '-p', '7687:7687',
                        '-e', 'NEO4J_AUTH=none',
                        '--name', cls.docker_container_name,
                        'neo4j'])

        print('waiting for db to be up')
        sleep(5)

    @classmethod
    def tearDownClass(cls):
        print('shutting down db')
        subprocess.run(['docker', 'stop', cls.docker_container_name])

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/', options={'swagger_ui': False})
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        return app.app
