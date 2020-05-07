# coding: utf-8

from __future__ import absolute_import

import json

from hypothesis import given, strategies as st, assume

from swagger_server.helpers import db
from swagger_server.test import BaseTestCase
from swagger_server.test.utils import cleanup_each_example

experiment_id_st = st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1)
samples_post_body_st = st.fixed_dictionaries({
    'experiment_id': experiment_id_st,
    'nearest-neighbours': st.lists(elements=st.fixed_dictionaries({
        'experiment_id': experiment_id_st,
        'distance': st.integers(min_value=-2 << 31, max_value=(2 << 31)-1)
    }), min_size=1),
})


class TestSampleController(BaseTestCase):

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
        expected_resp.pop('nearest-neighbours', None)
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
