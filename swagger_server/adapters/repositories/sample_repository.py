from swagger_server.adapters.databases.neo4j import INeo4jDatabase
from swagger_server.adapters.object_mappers.neo4j import SampleNode
from swagger_server.models import Sample


class SampleAlreadyExist(Exception):
    pass


class SampleRepository:

    def __init__(self, db: INeo4jDatabase):
        self.db = db

    def add(self, sample: Sample):
        node = SampleNode()
        node.name = sample.experiment_id

        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                neighbour_node = SampleNode()
                neighbour_node.name = neighbour.experiment_id
                node.neighbours.add(neighbour_node, distance=neighbour.distance)

        self.db.create(node)
