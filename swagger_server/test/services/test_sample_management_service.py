from hypothesis import given
from hypothesis.strategies import from_type

from swagger_server.models import Sample
from swagger_server.services import SampleManagementService
from swagger_server.services.sample_management import DuplicatedSample
from swagger_server.test import DBTestCase
from swagger_server.test.utils import cleanup_each_example


class SampleManagementServiceTestCase(DBTestCase):
    @given(sample=from_type(Sample))
    @cleanup_each_example
    def test_adding_duplicated_samples(self, sample):
        with self.assertRaises(DuplicatedSample):
            SampleManagementService.add(sample)
            SampleManagementService.add(sample)
