import unittest

from hypothesis import given, strategies as st, settings

from swagger_server.dal.neo4j import Neo4jDAL
from swagger_server.helpers import db
from swagger_server.test.dal import BaseDALTestCase
from swagger_server.test.dal.strategies import NEO4J_IDENTIFIER_ST, NEO4J_VALUE_ST
from swagger_server.test.utils import cleanup_each_example


class TestNodeDAL(BaseDALTestCase):
    @cleanup_each_example
    def test_creating_single_node(self):
        self.check_empty_db()

        node = Neo4jDAL.create_node()

        from_db = db.Neo4jDatabase.get().query('MATCH (n) RETURN n', write=True).values()[0][0]
        self.assertEqual(node['id'], from_db['id'])

    @given(label=NEO4J_IDENTIFIER_ST)
    @cleanup_each_example
    def test_creating_single_node_with_single_label(self, label):
        self.check_empty_db()

        node = Neo4jDAL.create_node(labels=[label])

        from_db = db.Neo4jDatabase.get().query('MATCH (n) RETURN n', write=True).values()[0][0]
        self.assertEqual(node['label'], from_db['label'])

    @given(labels=st.lists(elements=NEO4J_IDENTIFIER_ST, unique=True))
    @cleanup_each_example
    def test_creating_single_node_with_multiple_labels(self, labels):
        self.check_empty_db()

        node = Neo4jDAL.create_node(labels=labels)

        from_db = db.Neo4jDatabase.get().query('MATCH (n) RETURN n', write=True).values()[0][0]
        self.assertEqual(node['label'], from_db['label'])

    @given(properties=st.dictionaries(
        keys=NEO4J_IDENTIFIER_ST,
        values=NEO4J_VALUE_ST
    ))
    @settings(deadline=None)
    @cleanup_each_example
    def test_creating_single_node_with_properties(self, properties):
        self.check_empty_db()

        node = Neo4jDAL.create_node(properties=properties)

        from_db = db.Neo4jDatabase.get().query('MATCH (n) RETURN n', write=True).values()[0][0]
        for k in properties:
            self.assertEqual(node[k], from_db[k])

    def check_empty_db(self):
        rows = db.Neo4jDatabase.get().query('MATCH (n) RETURN n').values()
        self.assertEqual(len(rows), 0)


if __name__ == '__main__':
    unittest.main()
