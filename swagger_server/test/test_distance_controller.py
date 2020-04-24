# coding: utf-8

from __future__ import absolute_import

import json
from random import randrange
from unittest.mock import patch

from hypothesis import given, strategies as st, assume

from swagger_server.orm.DistanceORM import SampleNode, LineageNode
from swagger_server.test import BaseTestCase


class TestDistanceController(BaseTestCase):

    @given(sub_type=st.one_of(
        st.just('nearest-leaf-node'),
        st.just('nearest-neighbours')
    ), sample=st.text())
    def test_non_existing_sample(self, sub_type, sample):
        assume(sample != self.node.name)

        response = self.request("surely not in db", sub_type)

        self.assert404(response)
        self.assertDictEqual(
            json.loads(response.data.decode('utf-8')),
            {
                'code': 404,
                'message': "Not found"
            }
        )

    def test_nearest_leaf(self):
        response = self.request(self.node.name, 'nearest-leaf-node')

        self.assert200(response)
        self.assertDictEqual(
            json.loads(response.data.decode()),
            {
                'leaf_id': self.leaf.name,
                'distance': self.dist
            }
        )

    def test_nearest_neighbors(self):
        response = self.request(self.node.name, 'nearest-neighbours')

        self.assert200(response)

        actual = json.loads(response.data.decode())
        expected = [{
            'experiment_id': n.name,
            'distance': self.node.neighbors.relationship(n).dist
        } for n in self.neighbours]

        for a in actual:
            self.assertIn(a, expected)

    @given(sub_type=st.one_of(
        st.just('nearest-leaf-node'),
        st.just('nearest-neighbours')
    ))
    def test_unexpected_error(self, sub_type):
        with patch('swagger_server.controllers.distance_controller.Neighbour', side_effect=ValueError),\
             patch('swagger_server.controllers.distance_controller.NearestLeaf', side_effect=ValueError):
            response = self.request(self.node.name, sub_type)

        self.assert500(response)
        self.assertDictEqual(
            json.loads(response.data.decode('utf-8')),
            {
                'code': 500,
                'message': "Unexpected error"
            }
        )

    def request(self, experiment_id, sub_type):
        return self.client.open(
            '/api/v1/samples/{id}/{sub_type}'.format(id=experiment_id, sub_type=sub_type),
            method='GET'
        )

    def setUp(self):
        self.node = SampleNode(name='test node')
        self.node.save()

        self.neighbours = SampleNode.create(*[{'name': 'test neighbour %d' % i} for i in range(2)])
        for n in self.neighbours:
            self.node.neighbors.connect(n, {'dist': randrange(10)})

        self.leaf = LineageNode(name='test leaf')
        self.leaf.save()

        self.dist = 10
        self.node.lineage.connect(self.leaf, {'dist': self.dist})

    def tearDown(self):
        for n in self.neighbours:
            n.delete()
        self.leaf.delete()
        self.node.delete()


if __name__ == '__main__':
    import unittest
    unittest.main()
