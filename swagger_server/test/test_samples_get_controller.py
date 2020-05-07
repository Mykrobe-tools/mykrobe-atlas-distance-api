# coding: utf-8

from __future__ import absolute_import

from flask import json
from hypothesis import given

from swagger_server.helpers import db
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.test import BaseTestCase
from swagger_server.test.utils import experiment_id_st, cleanup_each_example


class TestSamplesGetController(BaseTestCase):

    @given(experiment_id=experiment_id_st)
    def test_getting_non_existent_sample(self, experiment_id):
        response = self.request(experiment_id)

        self.assert404(response)
        self.assertDictEqual(
            json.loads(response.data.decode()),
            Error(404, 'Not found').to_dict()
        )

    @given(experiment_id=experiment_id_st)
    @cleanup_each_example
    def test_getting_sample(self, experiment_id):
        db.Database.get().query(f'CREATE (:SampleNode {{name: "{experiment_id}"}})')

        response = self.request(experiment_id)

        self.assert200(response)
        self.assertDictEqual(
            json.loads(response.data.decode()),
            {k: v for k, v in Sample(experiment_id).to_dict().items() if v}
        )

    def request(self, experiment_id):
        return self.client.open(
            f'/api/v1/samples/{experiment_id}',
            method='GET'
        )


if __name__ == '__main__':
    import unittest
    unittest.main()
