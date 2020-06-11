from py2neo import Graph
from py2neo.ogm import GraphObject

from swagger_server.exceptions import Exists, NotFound


class GraphModel(GraphObject):
    def create(self, graph: Graph):
        if self.exists(graph):
            raise Exists

        graph.create(self)

    def update(self, graph: Graph):
        if not self.exists(graph):
            raise NotFound

        graph.push(self)

    @classmethod
    def get(cls, pk, graph: Graph):
        matched = cls.match(graph, pk).limit(1)

        if len(matched) == 0:
            raise NotFound

        return matched.first()

    def exists(self, graph: Graph):
        existing = self.match(graph).where(**{
            self.__primarykey__: self.__primaryvalue__
        })

        return len(existing) > 0

    @classmethod
    def delete(cls, pk, graph: Graph):
        node = cls.get(pk, graph)
        graph.delete(node)
