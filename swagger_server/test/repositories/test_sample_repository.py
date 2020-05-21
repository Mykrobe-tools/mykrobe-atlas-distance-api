from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text

from swagger_server.drivers.neo4j import Neo4jDriver
from swagger_server.repositories.sample_repository import create_sample
from swagger_server.test.utils import cleanup_each_example


class SampleRepositoryTestCase(TestCase):
    @given(name=text())
    @cleanup_each_example
    def test_create_sample(self, name):
        with Neo4jDriver.get() as driver:
            with driver.driver.session() as s:
                sample = s.write_transaction(create_sample, name)
                rows = s.read_transaction(
                    lambda tx: tx.run('MATCH (n:SampleNode {name: $name}) RETURN n', name=name)).values()

        self.assertEqual(name, sample.experiment_id)
        self.assertEqual(1, len(rows))
