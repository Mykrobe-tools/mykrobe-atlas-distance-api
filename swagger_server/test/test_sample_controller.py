# coding: utf-8

from __future__ import absolute_import

import json

from hypothesis import given, strategies as st, assume

from swagger_server.helpers import db
from swagger_server.test import BaseTestCase

experiment_id_st = st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1)


class TestSampleController(BaseTestCase):

    @given(body=st.one_of(
        st.fixed_dictionaries({
            'experiment_id': experiment_id_st
        }),
        st.fixed_dictionaries({
            'experiment_id': experiment_id_st,
            'nearest-neighbours': st.lists(elements=st.fixed_dictionaries({
                'experiment_id': experiment_id_st,
                'distance': st.integers(min_value=-2 << 31, max_value=(2 << 31)-1)
            })),
        })
    ))
    def test_creating_sample(self, body):
        experiment_ids = [body['experiment_id']] + [x['experiment_id'] for x in body.get('nearest-neighbours', [])]
        assume(len(set(experiment_ids)) == len(experiment_ids))

        response = self.request(body)

        rows = db.Database.get().query(
            f'MATCH '
            f'(n:SampleNode {{name: "{body["experiment_id"]}"}}) '
            f'OPTIONAL MATCH (n)-[r:NEIGHBOUR]->(m:SampleNode) '
            'RETURN n,r,m'
        ).values()
        db.Database.get().query('MATCH (n) DETACH DELETE n')

        self.assertEqual(response.status_code, 201)

        expected_resp = body.copy()
        if 'nearest-neighbours' in expected_resp and expected_resp['nearest-neighbours'] == []:
            del expected_resp['nearest-neighbours']
        self.assertDictEqual(
            json.loads(response.data.decode('utf-8')),
            expected_resp
        )

        if body.get('nearest-neighbours', []):
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

    @classmethod
    def setUpClass(cls):
        super().setUpClass()


if __name__ == '__main__':
    import unittest
    unittest.main()
