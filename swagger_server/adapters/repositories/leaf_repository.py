from swagger_server.adapters.databases.neo4j import Neo4jDatabase
from swagger_server.adapters.object_mappers.neo4j import LeafNode
from swagger_server.models import Leaf


class LeafAlreadyExist(Exception):
    pass


class LeafRepository:

    def __init__(self, db: Neo4jDatabase):
        self.db = db

    def add(self, leaf: Leaf):
        if LeafNode.primary_key_exists(leaf.leaf_id, self.db.graph):
            raise LeafAlreadyExist

        node = LeafNode()
        node.name = leaf.leaf_id

        self.db.create_or_merge(node)
