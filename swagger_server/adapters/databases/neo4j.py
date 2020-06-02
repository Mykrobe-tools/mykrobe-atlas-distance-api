from abc import ABC, abstractmethod

from py2neo import Graph, NodeMatcher, RelationshipMatcher
from py2neo.ogm import GraphObject

from swagger_server.adapters.databases.base import BaseDatabase


class INeo4jDatabase(ABC):
    @abstractmethod
    def create(self, obj: GraphObject):
        raise NotImplementedError


class Neo4jDatabase(BaseDatabase, INeo4jDatabase):

    def __init__(self, uri=None, **settings):
        self.graph = Graph(uri, **settings)

    @property
    def node_matcher(self) -> NodeMatcher:
        return self.graph.nodes

    @property
    def rel_matcher(self) -> RelationshipMatcher:
        return self.graph.relationships

    def create(self, obj: GraphObject):
        self.graph.create(obj)

    def truncate(self):
        self.graph.delete_all()
