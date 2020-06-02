from swagger_server.adapters.object_mappers.neo4j import SampleNode
from swagger_server.databases.exceptions import UniqueConstraintViolated
from swagger_server.databases.neo4j import INeo4jDatabase
from swagger_server.models import Sample


class SampleAlreadyExist(Exception):
    pass


class SampleRepository:

    def __init__(self, db: INeo4jDatabase):
        self.db = db

    def add(self, sample: Sample):
        node = SampleNode()
        node.name = sample.experiment_id

        try:
            self.db.create(node)
        except UniqueConstraintViolated:
            raise SampleAlreadyExist
