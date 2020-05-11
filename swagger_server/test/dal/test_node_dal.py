import unittest

from hypothesis import given, strategies as st, settings

from swagger_server.dal.neo4j import Neo4jNode
from swagger_server.helpers import db
from swagger_server.test.dal import BaseDALTestCase
from swagger_server.test.dal.strategies import NEO4J_IDENTIFIER_ST, NEO4J_VALUE_ST
from swagger_server.test.utils import cleanup_each_example


class TestNodeDAL(BaseDALTestCase):
    @cleanup_each_example
    def test_creating_single_node(self):
        self.check_empty_db()

        Neo4jNode()

        rows = db.Neo4jDatabase.get().query('MATCH (n) RETURN n').values()
        self.assertEqual(len(rows), 1)

    @given(label=NEO4J_IDENTIFIER_ST)
    @cleanup_each_example
    def test_creating_single_node_with_single_label(self, label):
        self.check_empty_db()

        Neo4jNode(labels=[label])

        rows = db.Neo4jDatabase.get().query(f'MATCH (n:{label}) RETURN n').values()
        self.assertEqual(len(rows), 1)

    @given(labels=st.lists(elements=NEO4J_IDENTIFIER_ST, unique=True, min_size=1))
    @settings(deadline=None)
    @cleanup_each_example
    def test_creating_single_node_with_multiple_labels(self, labels):
        self.check_empty_db()

        Neo4jNode(labels=labels)

        rows = db.Neo4jDatabase.get().query(f'MATCH (n:{":".join(labels)}) RETURN n').values()
        self.assertEqual(len(rows), 1)

    @given(properties=st.dictionaries(
        keys=NEO4J_IDENTIFIER_ST,
        values=NEO4J_VALUE_ST
    ))
    @settings(deadline=None)
    @cleanup_each_example
    def test_creating_single_node_with_properties(self, properties):
        self.check_empty_db()

        Neo4jNode(properties=properties)

        rows = db.Neo4jDatabase.get().query(f'MATCH (n) RETURN n', write=True).values()
        self.assertEqual(len(rows), 1)

        for k in rows[0][0]:
            if k in properties:
                v = properties[k]
                prop = rows[0][0][k]

                if isinstance(v, float):
                    self.assertAlmostEqual(prop, v)
                else:
                    self.assertEqual(prop, v)

    def check_empty_db(self):
        rows = db.Neo4jDatabase.get().query('MATCH (n) RETURN n').values()
        self.assertEqual(len(rows), 0)


if __name__ == '__main__':
    unittest.main()
