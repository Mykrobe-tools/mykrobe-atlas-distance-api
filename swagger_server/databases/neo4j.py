from py2neo import Graph, Schema, NodeMatcher, ClientError
from py2neo.ogm import GraphObject

from swagger_server.databases.base import BaseDatabase
from swagger_server.adapters.object_mappers.neo4j import SampleNode
from swagger_server.databases.exceptions import UniqueConstraintViolated


class Neo4JDatabase(BaseDatabase):

    def __init__(self, graph: Graph = None):
        self.graph = graph or Graph()

    @property
    def node_matcher(self) -> NodeMatcher:
        return self.graph.nodes

    def create(self, obj: GraphObject):
        tx = self.graph.begin()
        try:
            tx.create(obj.__node__)
        except ClientError as e:
            if 'already exist' in e.message:
                raise UniqueConstraintViolated
            raise e
        else:
            tx.commit()

    def apply_schema(self):
        schema = Schema(self.graph)

        if SampleNode.__primarykey__ not in schema.get_uniqueness_constraints(SampleNode.__primarylabel__):
            schema.create_uniqueness_constraint(SampleNode.__primarylabel__, SampleNode.__primarykey__)

    def truncate(self):
        self.graph.delete_all()
