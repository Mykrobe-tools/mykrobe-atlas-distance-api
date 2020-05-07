# coding: utf-8

from __future__ import absolute_import

from swagger_server.test import BaseTestCase
from swagger_server.test.utils import capture_logs


class TestSampleController(BaseTestCase):

    @capture_logs
    def test_missing_experiment_id(self):
        response = self.request({})
        self.assert400(response)

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
