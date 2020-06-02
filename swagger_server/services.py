from swagger_server.adapters.repositories.sample_repository import SampleRepository
from swagger_server.databases.base import BaseDatabase
from swagger_server.models import Sample


def add_new_sample(sample: Sample, db: BaseDatabase):
    repo = SampleRepository(db)
    repo.add(sample)
