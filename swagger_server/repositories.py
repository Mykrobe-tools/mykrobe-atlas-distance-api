from py2neo import Graph, Node
from py2neo.ogm import GraphObject

from swagger_server.exceptions import Exists


class Neo4jRepository:
    def __init__(self, driver: Graph):
        self.driver = driver

    def create(self, subgraph: GraphObject):
        if self.primary_key_exists(subgraph):
            raise Exists

        self.driver.create(subgraph)

    def primary_key_exists(self, subgraph: GraphObject):
        existing = subgraph.__class__.match(self.driver).where(**{
            subgraph.__primarykey__: subgraph.__primaryvalue__
        })

        return len(existing) > 0
