from unittest import TestCase

from hypothesis import given
from py2neo import Node

from swagger_server.drivers import Neo4jDriver
from swagger_server.drivers.exceptions import DriverError
from swagger_server.migrations import migrate
from swagger_server.migrations.neo4j import unique_sample_name
from swagger_server.ogm import SampleNode
from swagger_server.test.strategies import neo4j_strings
from swagger_server.test.utils import cleanup_each_example


class SampleNodeTestCase(TestCase):
    def setUp(self):
        try:
            Neo4jDriver.get().execute(unique_sample_name.BACKWARD)
        except DriverError:
            pass

    @given(name=neo4j_strings())
    @cleanup_each_example
    def test_unique_name_constraint(self, name):
        migrate()

        with self.assertRaises(DriverError):
            a = Node('SampleNode', name=name)
            b = Node('SampleNode', name=name)
            Neo4jDriver.get().create_new(a)
            Neo4jDriver.get().create_new(b)

    @given(name=neo4j_strings())
    @cleanup_each_example
    def test_unique_name_constraint_with_graph_objects(self, name):
        migrate()

        with self.assertRaises(DriverError):
            a = SampleNode(name=name)
            b = SampleNode(name=name)
            Neo4jDriver.get().create_new(a)
            Neo4jDriver.get().create_new(b)
