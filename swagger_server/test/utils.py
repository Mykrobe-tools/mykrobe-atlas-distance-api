from unittest import TestCase

from swagger_server.drivers.neo4j import Neo4jDriver
from swagger_server.migrate import migrate


class DBTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        with Neo4jDriver.get() as driver:
            migrate(driver.driver)
