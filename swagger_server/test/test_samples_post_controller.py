# coding: utf-8

from __future__ import absolute_import

import json

from hypothesis import given, strategies as st, assume, settings, HealthCheck

from swagger_server.helpers import db
from swagger_server.test import BaseTestCase
from swagger_server.test.utils import cleanup_each_example

experiment_id_st = st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1)
samples_post_body_st = st.fixed_dictionaries({
    'experiment_id': experiment_id_st,
    'nearest-neighbours': st.lists(elements=st.fixed_dictionaries({
        'experiment_id': experiment_id_st,
        'distance': st.integers(min_value=-2 ** 63, max_value=(2 ** 63)-1)
    }), min_size=1),
    'nearest-leaf-node': st.fixed_dictionaries({
        'leaf_id': experiment_id_st,
        'distance': st.integers(min_value=-2 ** 63, max_value=(2 ** 63)-1)
    })
})


class TestSamplesPostController(BaseTestCase):

    @given(body=st.one_of(
        st.fixed_dictionaries({
            'experiment_id': experiment_id_st
        }),
        st.fixed_dictionaries({
            'experiment_id': experiment_id_st,
            'nearest-neighbours': st.just([])
        })
    ))
    @cleanup_each_example
    def test_creating_isolated_sample(self, body):
        response = self.request(body)

        self.assertEqual(response.status_code, 201)

        expected_resp = body.copy()
        expected_resp['nearest-neighbours'] = []
        self.assertDictEqual(
            json.loads(response.data.decode('utf-8')),
            expected_resp
        )

        rows = self.get_nodes_and_relationships(body['experiment_id'])
        self.assertEqual(len(rows), 1)
        self.assertIsNone(rows[0][1])
        self.assertIsNone(rows[0][2])

    @given(body=samples_post_body_st)
    @cleanup_each_example
    def test_creating_sample(self, body):
        experiment_ids = [body['experiment_id']] + [x['experiment_id'] for x in body.get('nearest-neighbours', [])]
        assume(len(set(experiment_ids)) == len(experiment_ids))

        response = self.request(body)

        self.assertEqual(response.status_code, 201)

        self.assertDictEqual(
            json.loads(response.data.decode('utf-8')),
            body
        )

        rows = self.get_nodes_and_relationships(body['experiment_id'])
        neighbour_dists = {n['experiment_id']: n['distance'] for n in body['nearest-neighbours']}
        for row in rows:
            sample = row[0]
            self.assertEqual(sample['name'], body['experiment_id'])

            if 'nearest-neighbours' in body:
                rel = row[1]
                neighbour = row[2]

                self.assertIn(neighbour['name'], neighbour_dists)
                self.assertEqual(rel['dist'], neighbour_dists[neighbour['name']])

    @settings(suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow))
    @given(body=samples_post_body_st)
    @cleanup_each_example
    def test_creating_duplicated_samples(self, body):
        experiment_ids = [body['experiment_id']] + [x['experiment_id'] for x in body.get('nearest-neighbours', [])]
        assume(len(set(experiment_ids)) < len(experiment_ids))

        response = self.request(body)

        self.assertEqual(response.status_code, 409)

        rows = self.get_nodes_and_relationships(body['experiment_id'])
        self.assertEqual(len(rows), 0)

    @settings(suppress_health_check=(HealthCheck.filter_too_much, HealthCheck.too_slow))
    @given(body=samples_post_body_st, existed=experiment_id_st)
    @cleanup_each_example
    def test_creating_existed_samples(self, body, existed):
        experiment_ids = [body['experiment_id']] + [x['experiment_id'] for x in body.get('nearest-neighbours', [])]
        assume(len(set(experiment_ids)) == len(experiment_ids))
        assume(existed in experiment_ids)

        db.Database.get().query(f'CREATE (:SampleNode {{name: "{existed}"}})')

        response = self.request(body)

        self.assertEqual(response.status_code, 409)

        rows = self.get_nodes_and_relationships(body['experiment_id'])
        self.assertIn(len(rows), [0, 1])

    def request(self, body):
        return self.client.open(
            '/api/v1/samples',
            method='POST',
            json=body
        )

    @staticmethod
    def get_nodes_and_relationships(experiment_id):
        return db.Database.get().query(
            f'MATCH '
            f'(n:SampleNode {{name: "{experiment_id}"}}) '
            f'OPTIONAL MATCH (n)-[r:NEIGHBOUR]->(m:SampleNode) '
            'RETURN n,r,m'
        ).values()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()


if __name__ == '__main__':
    import unittest
    unittest.main()
