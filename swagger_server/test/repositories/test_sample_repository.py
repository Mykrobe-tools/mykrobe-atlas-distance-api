from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import from_type

from swagger_server.drivers import Neo4jDriver
from swagger_server.models import Sample
from swagger_server.repositories import SampleRepository
from swagger_server.test.utils import cleanup_each_example


class SampleRepositoryTestCase(TestCase):
    @given(sample=from_type(Sample))
    @cleanup_each_example
    def test_create_sample(self, sample):
        driver = Neo4jDriver.get()

        node = SampleRepository.create(sample)
        driver.apply_changes(node)

        self.assertTrue(driver.verify_changes(node))
