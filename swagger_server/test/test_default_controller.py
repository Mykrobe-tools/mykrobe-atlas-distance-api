# coding: utf-8

from __future__ import absolute_import

from unittest.mock import patch, MagicMock

from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_distance_post(self):
        """Test case for distance_post

        
        """
        mock_db = MagicMock()
        mock_db.cypher_query.return_value = ([], None)
        with patch('swagger_server.controllers.default_controller.db', new=mock_db):
            response = self.client.open(
                '/distance',
                method='POST',
                json={"experimental_id": "s1"},
                content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
