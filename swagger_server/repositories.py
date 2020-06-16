from typing import Type

from py2neo import Graph
from py2neo.ogm import GraphObject

from swagger_server.exceptions import Exists, NotFound


class BaseRepository:
    """
    Repositories provide high level abstractions for data persistence operations.
    """


class Neo4jRepository(BaseRepository):
    def __init__(self, driver: Graph = None, uri: str = None, **connection_settings):
        self.driver = driver or Graph(uri, **connection_settings)

    def create(self, graph_object: GraphObject):
        if self.exists(graph_object):
            raise Exists

        self.driver.create(graph_object)

    def update(self, graph_object: GraphObject):
        if not self.exists(graph_object):
            raise NotFound

        self.driver.push(graph_object)

    def get(self, graph_object_class: Type[GraphObject], pk) -> GraphObject:
        matched = graph_object_class.match(self.driver, pk).limit(1)

        if len(matched) == 0:
            raise NotFound

        return matched.first()

    def exists(self, graph_object: GraphObject):
        existing = graph_object.__class__.match(self.driver).where(**{
            graph_object.__primarykey__: graph_object.__primaryvalue__
        })

        return len(existing) > 0

    def delete(self, graph_object_class: Type[GraphObject], pk):
        node = self.get(graph_object_class, pk)
        self.driver.delete(node)

    def truncate(self):
        self.driver.delete_all()
