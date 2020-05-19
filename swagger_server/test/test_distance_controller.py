# coding: utf-8

from __future__ import absolute_import

import json
import logging
from random import randrange
from unittest.mock import patch

from hypothesis import given, strategies as st, assume

from swagger_server.helpers import db
from swagger_server.test import BaseTestCase


class TestDistanceController(BaseTestCase):

    @given(sub_type=st.one_of(
        st.just('nearest-leaf-node'),
        st.just('nearest-neighbours')
    ), sample=st.text())
    def test_non_existing_sample(self, sub_type, sample):
        assume(sample != self.node['name'])

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
        response = self.request(self.node['name'], 'nearest-leaf-node')

        self.assert200(response)
        self.assertDictEqual(
            json.loads(response.data.decode()),
            {
                'leaf_id': self.leaf['name'],
                'distance': self.dist
            }
        )

    def test_no_nearest_leaf(self):
        response = self.request(self.isolated_node_name, 'nearest-leaf-node')

        self.assert404(response)

    def test_nearest_neighbors(self):
        response = self.request(self.node['name'], 'nearest-neighbours')

        self.assert200(response)

        actual = json.loads(response.data.decode())
        expected = [{
            'experiment_id': n['name'],
            'distance': d
        } for n, d in zip(self.neighbours, self.neighbour_dists)]

        for a in actual:
            self.assertIn(a, expected)

    def test_no_neighbor(self):
        response = self.request(self.isolated_node_name, 'nearest-neighbours')

        self.assert404(response)

    @given(sub_type=st.one_of(
        st.just('nearest-leaf-node'),
        st.just('nearest-neighbours')
    ))
    def test_unexpected_error(self, sub_type):
        with patch('swagger_server.controllers.distance_controller.Neighbour', side_effect=ValueError),\
             patch('swagger_server.controllers.distance_controller.NearestLeaf', side_effect=ValueError),\
             self.assertLogs(level=logging.ERROR):
            response = self.request(self.node['name'], sub_type)

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

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.dist = 10
        cls.neighbour_dists = [randrange(10), randrange(10)]
        query = 'create ' \
                '(a:SampleNode {{name: "test node"}}),' \
                '(b:SampleNode {{name: "test neighbour 1"}}),' \
                '(c:SampleNode {{name: "test neighbour 2"}}),' \
                '(d:LineageNode {{name: "test leaf"}}),' \
                '(a)-[:NEIGHBOUR {{dist: {d1}}}]->(b), (a)-[:NEIGHBOUR {{dist: {d2}}}]->(c),' \
                '(a)-[:LINEAGE {{dist: {d3}}}]->(d) ' \
                'return a,b,c,d'

        rows = db.Neo4jDatabase.get().query(query.format(d1=cls.neighbour_dists[0], d2=cls.neighbour_dists[1], d3=cls.dist)).values()
        cls.node = rows[0][0]
        cls.neighbours = rows[0][1:3]
        cls.leaf = rows[0][3]

        cls.isolated_node_name = 'isolated'
        db.Neo4jDatabase.get().query(f'create (n:SampleNode {{name: "{cls.isolated_node_name}"}})')


if __name__ == '__main__':
    import unittest
    unittest.main()
