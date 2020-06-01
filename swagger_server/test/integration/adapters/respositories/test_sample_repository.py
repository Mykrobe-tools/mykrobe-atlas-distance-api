from hypothesis import given
from hypothesis.strategies import from_type

from swagger_server.adapters.repositories.sample_repository import SampleRepository
from swagger_server.models import Sample
from swagger_server.test.fixtures import managed_db


@given(sample=from_type(Sample))
def test_adding_new_sample(sample):
    with managed_db() as db:
        repo = SampleRepository(db)

        repo.add(sample)

        assert len(db.nodes.match('SampleNode', name=sample.experiment_id)) == 1
