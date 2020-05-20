from swagger_server.helpers import db
from swagger_server.test import BaseTestCase


class DALTestCase(BaseTestCase):
    def test_creating_self_referencing_relationship(self):
        db.Neo4jDatabase.get().query('CREATE (n)-[:EDGE]->(n)')
