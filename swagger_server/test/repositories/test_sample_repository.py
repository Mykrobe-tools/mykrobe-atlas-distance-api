from hypothesis import given, assume
from hypothesis.strategies import from_type, lists
from neobolt.exceptions import ConstraintError

from swagger_server.drivers.neo4j import Neo4jDriver
from swagger_server.models import Sample, Neighbour
from swagger_server.repositories.sample_repository import create_or_update_sample, create_sample
from swagger_server.test.decorators import cleanup_each_example
from swagger_server.test.strategies import experiment_ids
from swagger_server.test.utils import DBTestCase


class SampleRepositoryTestCase(DBTestCase):
    @given(name=experiment_ids())
    @cleanup_each_example
    def test_create_sample(self, name):
        sample = Sample(name)

        with Neo4jDriver.get() as driver:
            with driver.driver.session() as s:
                s.write_transaction(create_sample, sample)

                all_nodes_with_said_name = s.read_transaction(
                    lambda tx: tx.run('MATCH (n:SampleNode {name: $name}) RETURN n', name=name)).values()

        self.assertEqual(1, len(all_nodes_with_said_name))

    @given(name=experiment_ids())
    @cleanup_each_example
    def test_create_sample_twice(self, name):
        sample = Sample(name)

        with Neo4jDriver.get() as driver:
            with driver.driver.session() as s:
                with self.assertRaises(ConstraintError):
                    s.write_transaction(create_sample, sample)
                    s.write_transaction(create_sample, sample)

    @given(name=experiment_ids())
    @cleanup_each_example
    def test_create_or_update_sample(self, name):
        sample = Sample(name)

        with Neo4jDriver.get() as driver:
            with driver.driver.session() as s:
                s.write_transaction(create_sample, sample)
                s.write_transaction(create_or_update_sample, sample)

                all_nodes_with_said_name = s.read_transaction(
                    lambda tx: tx.run('MATCH (n:SampleNode {name: $name}) RETURN n', name=name)).values()

        self.assertEqual(1, len(all_nodes_with_said_name))

    @given(name=experiment_ids(), neighbours=lists(from_type(Neighbour)))
    @cleanup_each_example
    def test_create_sample_with_neighbours(self, name, neighbours):
        names = [name] + [n.experiment_id for n in neighbours]
        assume(len(set(names)) == len(names))

        sample = Sample(name, neighbours)

        with Neo4jDriver.get() as driver:
            with driver.driver.session() as s:
                s.write_transaction(create_or_update_sample, sample)

                all_neighbours = s.read_transaction(lambda tx: tx.run(
                    'MATCH (n:SampleNode {name: $name})-[e:NEIGHBOUR]->(ne:SampleNode) RETURN n,e,ne', name=name))\
                    .values()

        self.assertEqual(len(neighbours), len(all_neighbours))

        distances = {n.experiment_id: n.distance for n in neighbours}
        for row in all_neighbours:
            neighbour_name = row[2]['name']
            neighbour_distance = distances[neighbour_name]
            self.assertEqual(neighbour_distance, row[1]['dist'])
