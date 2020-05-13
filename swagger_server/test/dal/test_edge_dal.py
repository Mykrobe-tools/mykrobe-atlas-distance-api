import unittest

from hypothesis import given, assume, strategies as st, settings

from swagger_server.dal.neo4j import Neo4jNode, Neo4jPropertyMapping
from swagger_server.helpers import db
from swagger_server.test.dal import BaseDALTestCase
from swagger_server.test.dal.strategies import NEO4J_EDGE_ST
from swagger_server.test.utils import cleanup_each_example


class TestEdgeDAL(BaseDALTestCase):

    @given(edges=st.lists(NEO4J_EDGE_ST))
    @settings(deadline=None)
    @cleanup_each_example
    def test_connect_to_nodes(self, edges):
        labels = [label for label, _, _ in edges]
        assume(len(labels) == len(set(labels)))
        self.check_empty_db()

        a = Neo4jNode()
        for label, properties, (node_labels, node_props) in edges:
            n = Neo4jNode(node_labels, node_props)
            a.connect(n, label, properties)
        a.create()

        for label, properties, _ in edges:
            properties = Neo4jPropertyMapping(properties)
            rows = db.Neo4jDatabase.get().query(f'MATCH (n)-[:{label} {properties}]->() RETURN n').values()
            self.assertEqual(1, len(rows))

        rows = db.Neo4jDatabase.get().query(f'MATCH (n) RETURN n').values()
        self.assertEqual(len(edges) + 1, len(rows))


if __name__ == '__main__':
    unittest.main()
