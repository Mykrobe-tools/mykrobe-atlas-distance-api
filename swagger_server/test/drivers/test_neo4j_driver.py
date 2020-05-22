from concurrent.futures.thread import ThreadPoolExecutor
from unittest import TestCase

from swagger_server.drivers import Neo4jDriver


class Neo4jDriverTestCase(TestCase):
    def test_driver_implement_singleton_pattern(self):
        self.assertIs(Neo4jDriver.get(), Neo4jDriver.get())

    def test_singleton_instance_across_threads(self):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(lambda: Neo4jDriver.get())
        self.assertIs(Neo4jDriver.get(), future.result())
