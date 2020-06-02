from py2neo import Graph, Schema, NodeMatcher
from py2neo.ogm import GraphObject

from swagger_server.databases.base import BaseDatabase
from swagger_server.adapters.object_mappers.neo4j import SampleNode


class Neo4JDatabase(BaseDatabase):

    def __init__(self, graph: Graph = None):
        self.graph = graph or Graph()

    @property
    def node_matcher(self) -> NodeMatcher:
        return self.graph.nodes

    def create(self, obj: GraphObject):
        self.graph.create(obj)

    def apply_schema(self):
        schema = Schema(self.graph)

        if SampleNode.__primarykey__ not in schema.get_uniqueness_constraints(SampleNode.__primarylabel__):
            schema.create_uniqueness_constraint(SampleNode.__primarylabel__, SampleNode.__primarykey__)

    def truncate(self):
        self.graph.delete_all()
