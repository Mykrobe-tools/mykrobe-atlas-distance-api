# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSamplesGetController(BaseTestCase):
    """SamplesGetController integration test stubs"""

    def test_samples_id_get(self):
        """Test case for samples_id_get

        
        """
        response = self.client.open(
            '/api/v1/samples/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
