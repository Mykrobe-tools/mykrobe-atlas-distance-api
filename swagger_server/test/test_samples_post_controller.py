# coding: utf-8

from __future__ import absolute_import

from flask import json
from hypothesis import given
from hypothesis.strategies import from_type

from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.repositories import SampleRepository
from swagger_server.test import BaseTestCase
from swagger_server.test.utils import cleanup_each_example


class TestSamplesPostController(BaseTestCase):

    @given(sample=from_type(Sample))
    @cleanup_each_example
    def test_sample_already_existed(self, sample):
        SampleRepository.add(sample)

        response = self.request(sample)

        self.assertEqual(409, response.status_code)
        self.assertFalse(SampleRepository.exists(sample))

    def request(self, body):
        return self.client.open(
            '/api/v1/samples',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')


if __name__ == '__main__':
    import unittest
    unittest.main()
