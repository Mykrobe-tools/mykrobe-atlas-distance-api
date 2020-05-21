from concurrent.futures.thread import ThreadPoolExecutor
from unittest import TestCase
from unittest.mock import patch, MagicMock

from swagger_server.drivers.neo4j import Neo4jDriver


class Neo4jDriverTestCase(TestCase):
    def test_driver_implement_singleton_pattern(self):
        self.assertIs(Neo4jDriver.get(), Neo4jDriver.get())

    def test_singleton_instance_across_threads(self):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(lambda: Neo4jDriver.get())
        self.assertIs(Neo4jDriver.get(), future.result())

    def test_connection_management_via_context_manager(self):
        instance = Neo4jDriver.get()
        self.assertFalse(hasattr(instance, 'driver'))

        mock_driver = MagicMock()
        with patch('swagger_server.drivers.neo4j.GraphDatabase.driver', return_value=mock_driver), instance:
            self.assertIs(mock_driver, instance.driver)
            mock_driver.assert_not_called()

        mock_driver.close.assert_called()
