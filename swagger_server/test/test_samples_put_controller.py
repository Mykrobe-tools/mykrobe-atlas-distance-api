# coding: utf-8

from __future__ import absolute_import

from flask import json
from hypothesis import given, assume, settings
from hypothesis.strategies import lists, from_type

from swagger_server.helpers import db
from swagger_server.models.neighbour import Neighbour  # noqa: E501
from swagger_server.test import BaseTestCase
from swagger_server.test.utils import cleanup_each_example


class TestSamplePutController(BaseTestCase):

    @given(node=from_type(Neighbour), neighbours=lists(elements=from_type(Neighbour)))
    def test_non_existent_sample(self, node, neighbours):
        response = self.request(node.experiment_id, neighbours)
        self.assert404(response)

    @given(node=from_type(Neighbour), old_neighbours=lists(elements=from_type(Neighbour)), new_neighbours=lists(elements=from_type(Neighbour)))
    @settings(deadline=None)
    @cleanup_each_example
    def test_update_neighbours(self, node, old_neighbours, new_neighbours):
        ids = [n.experiment_id for n in [node] + old_neighbours + new_neighbours]
        assume(len(set(ids)) == len(ids))

        self.create_sample(node.experiment_id, old_neighbours)

        response = self.request(node.experiment_id, new_neighbours)

        self.assert200(response)
        self.check_neighbours(node.experiment_id, new_neighbours)

    def create_sample(self, experiment_id, neighbours):
        q = f'CREATE (n:SampleNode {{name: "{experiment_id}"}})'
        for n in neighbours:
            q += f',(n)-[:NEIGHBOUR {{dist: {n.distance}}}]->(:SampleNode {{name: "{n.experiment_id}"}})'

        db.Neo4jDatabase.get().query(q, write=True)

    def check_neighbours(self, experiment_id, neighbours):
        rows = db.Neo4jDatabase.get().query(
            f'MATCH (:SampleNode {{name: "{experiment_id}"}})-[e:NEIGHBOUR]->(n:SampleNode) RETURN e,n').values()

        self.assertEqual(len(neighbours), len(rows))

        distances = {r[1]['name']: r[0]['dist'] for r in rows}
        for n in neighbours:
            self.assertEqual(n.distance, distances[n.experiment_id])

    def request(self, experiment_id, neighbours):
        return self.client.open(
            '/api/v1/samples/{id}/nearest-neighbours'.format(id=experiment_id),
            method='PUT',
            data=json.dumps(neighbours),
            content_type='application/json')


if __name__ == '__main__':
    import unittest
    unittest.main()
