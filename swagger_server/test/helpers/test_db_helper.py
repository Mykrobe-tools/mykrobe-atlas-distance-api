from swagger_server.helpers import db
from swagger_server.test import BaseTestCase


class DBHelperTestCase(BaseTestCase):
    def test_throwing_error_if_not_use_in_context_manager(self):
        with self.assertRaises(RuntimeError):
            db.Neo4jDatabase.get().query('')
