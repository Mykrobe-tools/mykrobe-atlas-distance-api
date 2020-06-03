from swagger_server.adapters.databases.base import IDatabase
from swagger_server.adapters.repositories.sample_repository import SampleRepository, SampleAlreadyExist
from swagger_server.models import Sample


class ResourceAlreadyExist(Exception):
    pass


def add_new_sample(sample: Sample, db: IDatabase):
    repo = SampleRepository(db)

    try:
        repo.add(sample)
    except SampleAlreadyExist:
        raise ResourceAlreadyExist
