from unittest import TestCase

from swagger_server.helpers import db


class DBHelperTestCase(TestCase):
    def test_throwing_error_if_not_use_in_context_manager(self):
        with self.assertRaises(RuntimeError):
            db.Neo4jDatabase.get().query('')
