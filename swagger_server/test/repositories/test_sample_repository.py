from hypothesis import given
from hypothesis.strategies import from_type

from swagger_server.models import Sample
from swagger_server.repositories import SampleRepository
from swagger_server.repositories.sample_repository import SampleAlreadyExisted
from swagger_server.test import DBTestCase
from swagger_server.test.utils import cleanup_each_example


class SampleRepositoryTestCase(DBTestCase):
    @given(sample=from_type(Sample))
    @cleanup_each_example
    def test_adding_duplicated_samples(self, sample):
        with self.assertRaises(SampleAlreadyExisted):
            SampleRepository.add(sample)
            SampleRepository.add(sample)
