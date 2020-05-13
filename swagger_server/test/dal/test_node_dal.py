import unittest

from hypothesis import given, strategies as st, settings

from swagger_server.dal.neo4j import Neo4jNode, Neo4jLabelList
from swagger_server.helpers import db
from swagger_server.test.dal import BaseDALTestCase
from swagger_server.test.dal.strategies import NEO4J_IDENTIFIER_ST, NEO4J_PROPS_ST, NEO4J_LABELS_ST, \
    NEO4J_NODE_ST
from swagger_server.test.utils import cleanup_each_example


class TestNodeDAL(BaseDALTestCase):
    def test_creating_single_node(self):
        self.check_empty_db()

        Neo4jNode().create()

        rows = db.Neo4jDatabase.get().query('MATCH (n) RETURN n').values()
        self.assertEqual(1, len(rows))

    @given(label=NEO4J_IDENTIFIER_ST)
    @cleanup_each_example
    def test_creating_single_node_with_single_label(self, label):
        self.check_empty_db()

        Neo4jNode(labels=[label]).create()

        rows = db.Neo4jDatabase.get().query(f'MATCH (n:{label}) RETURN n').values()
        self.assertEqual(1, len(rows))

    @given(labels=NEO4J_LABELS_ST)
    @settings(deadline=None)
    @cleanup_each_example
    def test_creating_single_node_with_multiple_labels(self, labels):
        self.check_empty_db()

        Neo4jNode(labels=labels).create()

        rows = db.Neo4jDatabase.get().query(f'MATCH (n{Neo4jLabelList(labels)}) RETURN n').values()
        self.assertEqual(1, len(rows))

    @given(properties=NEO4J_PROPS_ST)
    @settings(deadline=None)
    @cleanup_each_example
    def test_creating_single_node_with_properties(self, properties):
        self.check_empty_db()

        Neo4jNode(properties=properties).create()

        rows = db.Neo4jDatabase.get().query(f'MATCH (n) RETURN n').values()
        self.assertEqual(1, len(rows))

        for k in rows[0][0]:
            if k in properties:
                v = properties[k]
                prop = rows[0][0][k]

                if isinstance(v, float):
                    self.assertAlmostEqual(v, prop)
                else:
                    self.assertEqual(v, prop)

    @given(nodes=st.lists(elements=NEO4J_NODE_ST))
    @settings(deadline=None)
    @cleanup_each_example
    def test_creating_multiple_nodes(self, nodes):
        self.check_empty_db()

        nodes = [Neo4jNode(labels, props) for labels, props in nodes]
        Neo4jNode.bulk_create(nodes)

        for n in nodes:
            rows = db.Neo4jDatabase.get().query(f'MATCH (n{n.labels} {n.properties}) RETURN n').values()
            self.assertGreaterEqual(len(rows), 1)


if __name__ == '__main__':
    unittest.main()
