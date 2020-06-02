from swagger_server.models import Sample
from swagger_server.databases.neo4j import Neo4JDatabase
from swagger_server.adapters.object_mappers.neo4j import SampleNode


class SampleRepository:

    def __init__(self, db: Neo4JDatabase):
        self.db = db

    def add(self, sample: Sample):
        node = SampleNode()
        node.name = sample.experiment_id

        self.db.create(node)
