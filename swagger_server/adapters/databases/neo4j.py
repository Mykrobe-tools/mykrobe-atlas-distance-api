from abc import ABC, abstractmethod

from py2neo import Graph
from py2neo.ogm import GraphObject

from swagger_server.adapters.databases.base import IDatabase


class INeo4jDatabase(ABC):
    @abstractmethod
    def create(self, obj: GraphObject):
        raise NotImplementedError


class Neo4jDatabase(IDatabase, INeo4jDatabase):

    def __init__(self, uri=None, **settings):
        self.graph = Graph(uri, **settings)

    def create(self, obj: GraphObject):
        tx = self.graph.begin()
        try:
            tx.create(obj)
        except Exception:
            raise
        else:
            tx.commit()

    def truncate(self):
        self.graph.delete_all()
