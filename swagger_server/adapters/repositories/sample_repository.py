from swagger_server.adapters.databases.base import IDatabase
from swagger_server.adapters.databases.neo4j import Neo4jDatabase
from swagger_server.adapters.object_mappers.neo4j import SampleNode
from swagger_server.models import Sample


class SampleAlreadyExist(Exception):
    pass


class SampleRepository:

    def __init__(self, db: IDatabase):
        self.db: Neo4jDatabase = db

    def add(self, sample: Sample):
        if SampleNode.primary_key_exists(sample.experiment_id, self.db.graph):
            raise SampleAlreadyExist

        node = SampleNode.from_model(sample)

        self.db.create_or_merge(node)
