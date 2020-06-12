from typing import Type

from py2neo import Graph
from py2neo.ogm import GraphObject

from swagger_server.exceptions import Exists, NotFound


class Neo4jRepository:
    def __init__(self, driver: Graph = None):
        self.driver = driver or Graph()

    def create(self, graph_object: GraphObject):
        if self.exists(graph_object):
            raise Exists

        self.driver.create(graph_object)

    def update(self, graph_object: GraphObject):
        if not self.exists(graph_object):
            raise NotFound

        self.driver.push(graph_object)

    def get(self, graph_object_class: Type[GraphObject], pk):
        matched = graph_object_class.match(self.driver, pk).limit(1)

        if len(matched) == 0:
            raise NotFound

        return matched.first()

    def exists(self, graph_object: GraphObject):
        existing = graph_object.__class__.match(self.driver).where(**{
            graph_object.__primarykey__: graph_object.__primaryvalue__
        })

        return len(existing) > 0

    def delete(self, pk, graph_object: GraphObject):
        node = self.get(pk, graph_object)
        self.driver.delete(node)

    def truncate(self):
        self.driver.delete_all()
