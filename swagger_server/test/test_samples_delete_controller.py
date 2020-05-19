# coding: utf-8

from __future__ import absolute_import

from flask import json
from hypothesis import given

from swagger_server.helpers import db
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase
from swagger_server.test.utils import experiment_id_st, cleanup_each_example


class TestSamplesDeleteController(BaseTestCase):

    @given(experiment_id=experiment_id_st)
    def test_deleting_non_existent_sample(self, experiment_id):
        response = self.request(experiment_id)

        self.assert404(response)
        self.assertDictEqual(
            json.loads(response.data.decode()),
            Error(404, 'Not found').to_dict()
        )

    @given(experiment_id=experiment_id_st)
    @cleanup_each_example
    def test_deleting_sample(self, experiment_id):
        db.Neo4jDatabase.get().query(f'CREATE (a:SampleNode {{name: "{experiment_id}"}}),'
                                f'(a)-[:NEIGHBOUR]->(:SampleNode), (a)-[:LINEAGE]->(:LineageNode)')

        response = self.request(experiment_id)

        self.assertEqual(response.status_code, 204)

        rows = db.Neo4jDatabase.get().query(f'MATCH (n:SampleNode {{name: "{experiment_id}"}}) RETURN n').values()
        self.assertEqual(len(rows), 0)

    def request(self, experiment_id):
        return self.client.open(
            f'/api/v1/samples/{experiment_id}',
            method='DELETE'
        )


if __name__ == '__main__':
    import unittest
    unittest.main()
