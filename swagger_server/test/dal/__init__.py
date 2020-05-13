from unittest import TestCase

from swagger_server.helpers import db


class BaseDALTestCase(TestCase):
    docker_container_name = 'test_neo4j'

    @classmethod
    def setUpClass(cls):
        db.URI = "bolt://localhost:7687"
        db.ENCRYPTED = False

    @classmethod
    def tearDownClass(cls):
        db.Neo4jDatabase.get().query('MATCH (n) DETACH DELETE n', write=True)

    def tearDown(self):
        db.Neo4jDatabase.get().query('MATCH (n) DETACH DELETE n', write=True)

    def check_empty_db(self):
        rows = db.Neo4jDatabase.get().query('MATCH (n) RETURN n').values()
        self.assertEqual(len(rows), 0)
