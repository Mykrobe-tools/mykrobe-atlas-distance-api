from swagger_server.models import Sample
from swagger_server.repositories import SampleRepository
from swagger_server.repositories.sample_repository import SampleAlreadyExisted


class DuplicatedSample(Exception):
    pass


class SampleManagementService:
    @staticmethod
    def add(sample: Sample):
        try:
            SampleRepository.add(sample)
        except SampleAlreadyExisted:
            raise DuplicatedSample
