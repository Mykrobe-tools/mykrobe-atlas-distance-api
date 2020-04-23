# coding: utf-8

from __future__ import absolute_import

import json
from unittest.mock import patch, MagicMock

from hypothesis import given, strategies as st, assume

from swagger_server.test import BaseTestCase

REL_TYPES = ['nearest-neighbor', 'nearest-leaf-node']


class TestDefaultController(BaseTestCase):

    @given(sub_type=st.text())
    def test_invalid_subtype(self, sub_type):
        assume(sub_type not in REL_TYPES)

        response = self.request(
            json={"experimental_id": "s1", "sub_type": sub_type})

        self.assert400(response)
        self.assertEqual(response.data.decode('utf-8'), '\"Invalid sub_type\"\n')

    @given(sub_type=st.just(REL_TYPES[0]))
    def test_nearest_neighbor(self, sub_type):
        mock_result = [
            [{'name': 's2'}, 1],
            [{'name': 's3'}, 2]
        ]
        mock_db = MagicMock()
        mock_db.cypher_query.return_value = (
            mock_result,
            None
        )

        with patch('swagger_server.controllers.default_controller.db', new=mock_db):
            response = self.request(json={"experimental_id": "s1", "sub_type": sub_type})

        self.assert200(response)
        self.assertDictEqual(json.loads(response.data.decode()), self.response(
            sub_type,
            {r[0]['name']: r[1] for r in mock_result}
        ))

    @given(sub_type=st.just(REL_TYPES[1]))
    def test_nearest_leaf(self, sub_type):
        mock_result = [
            [{'name': 's2'}],
            [{'name': 's3'}]
        ]
        mock_db = MagicMock()
        mock_db.cypher_query.return_value = (
            mock_result,
            None
        )

        with patch('swagger_server.controllers.default_controller.db', new=mock_db):
            response = self.request(json={"experimental_id": "s1", "sub_type": sub_type})

        self.assert200(response)
        self.assertDictEqual(json.loads(response.data.decode()), self.response(
            sub_type,
            {r[0]['name']: '' for r in mock_result}
        ))

    def request(self, json):
        return self.client.open(
                '/distance',
                method='POST',
                json=json,
                content_type='application/json')

    def response(self, sub_type, result, request_type='distance'):
        return {
            'type': request_type,
            'subType': sub_type,
            'result': result
        }


if __name__ == '__main__':
    import unittest
    unittest.main()
