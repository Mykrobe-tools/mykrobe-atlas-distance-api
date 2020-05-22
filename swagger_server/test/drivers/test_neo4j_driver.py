from hypothesis import given
from py2neo import Node

from swagger_server.drivers import Neo4jDriver
from swagger_server.drivers.exceptions import UniqueConstraintViolation
from swagger_server.ogm import SampleNode
from swagger_server.test import DBTestCase
from swagger_server.test.strategies import neo4j_strings
from swagger_server.test.utils import cleanup_each_example


class Neo4jDriverTestCase(DBTestCase):

    @given(name=neo4j_strings())
    @cleanup_each_example
    def test_unique_constraint_violation(self, name):
        with self.assertRaises(UniqueConstraintViolation):
            a = Node('SampleNode', name=name)
            b = Node('SampleNode', name=name)
            Neo4jDriver.get().create_new(a)
            Neo4jDriver.get().create_new(b)

    @given(name=neo4j_strings())
    @cleanup_each_example
    def test_unique_constraint_violation_with_graph_objects(self, name):
        with self.assertRaises(UniqueConstraintViolation):
            a = SampleNode(name=name)
            b = SampleNode(name=name)
            Neo4jDriver.get().create_new(a)
            Neo4jDriver.get().create_new(b)
