from swagger_server.drivers import Neo4jDriver
from swagger_server.drivers.exceptions import UniqueConstraintViolation
from swagger_server.models import Sample
from swagger_server.ogm import SampleNode


class SampleAlreadyExisted(Exception):
    pass


class SampleRepository:
    @staticmethod
    def add(sample: Sample):
        node = SampleNode(sample)
        try:
            Neo4jDriver.get().create_new(node)
        except UniqueConstraintViolation:
            raise SampleAlreadyExisted

    @staticmethod
    def exists(sample: Sample) -> bool:
        node = SampleNode(sample)
        return Neo4jDriver.get().verify_changes(node)
