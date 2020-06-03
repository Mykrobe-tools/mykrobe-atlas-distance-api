from swagger_server.adapters.databases.neo4j import Neo4jDatabase
from swagger_server.adapters.object_mappers.neo4j import SampleNode, LeafNode
from swagger_server.models import Sample


class SampleAlreadyExist(Exception):
    pass


class SampleRepository:

    def __init__(self, db: Neo4jDatabase):
        self.db = db

    def add(self, sample: Sample):
        if SampleNode.primary_key_exists(sample.experiment_id, self.db.graph):
            raise SampleAlreadyExist

        node = SampleNode()
        node.name = sample.experiment_id

        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                neighbour_node = SampleNode()
                neighbour_node.name = neighbour.experiment_id
                node.neighbours.add(neighbour_node, distance=neighbour.distance)

        if sample.nearest_leaf_node:
            leaf_node = LeafNode()
            leaf_node.name = sample.nearest_leaf_node.leaf_id
            node.lineage.add(leaf_node, distance=sample.nearest_leaf_node.distance)

        self.db.create_or_merge(node)
