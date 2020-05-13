import unittest

from hypothesis import given, strategies as st

from swagger_server.dal.neo4j import Neo4jNode
from swagger_server.helpers import db
from swagger_server.test.dal import BaseDALTestCase
from swagger_server.test.dal.strategies import NEO4J_IDENTIFIER_ST
from swagger_server.test.utils import cleanup_each_example


class TestEdgeDAL(BaseDALTestCase):

    @given(labels=st.lists(NEO4J_IDENTIFIER_ST, unique=True))
    @cleanup_each_example
    def test_connect_to_nodes(self, labels):
        self.check_empty_db()

        a = Neo4jNode()
        for label in labels:
            n = Neo4jNode()
            a.connect(n, label)
        a.create()

        for label in labels:
            rows = db.Neo4jDatabase.get().query(f'MATCH (n)-[:{label}]->() RETURN n').values()
            self.assertEqual(1, len(rows))


if __name__ == '__main__':
    unittest.main()
