from typing import Union

from py2neo import Graph, Subgraph
from py2neo.ogm import GraphObject

from swagger_server.drivers.base import BaseDriver


GraphState = Union[Subgraph, GraphObject]


class Neo4jDriver(BaseDriver):
    uri = 'bolt://localhost:7687'
    encrypted = False

    @classmethod
    def make_instance(cls) -> Union['Neo4jDriver']:
        return Neo4jDriver()

    def __init__(self):
        self.graph = Graph(self.uri, secure=self.encrypted)

    def apply_changes(self, changes: GraphState):
        self.graph.push(changes)

    def verify_changes(self, changes: GraphState) -> bool:
        return self.graph.exists(changes)

    def clear_db(self):
        self.graph.delete_all()
