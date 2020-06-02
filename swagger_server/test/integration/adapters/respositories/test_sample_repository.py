from pytest import raises

from swagger_server.adapters.repositories.sample_repository import SampleRepository, SampleAlreadyExist
from swagger_server.databases.exceptions import UniqueConstraintViolated
from swagger_server.databases.neo4j import INeo4jDatabase
from swagger_server.models import Sample


class FakeDatabase(INeo4jDatabase):
    def create(self, sample: Sample):
        raise UniqueConstraintViolated


def test_wrapping_unique_constraint_violation_in_more_domain_relevant_error():
    db = FakeDatabase()
    repo = SampleRepository(db)

    with raises(SampleAlreadyExist):
        repo.add(Sample())
