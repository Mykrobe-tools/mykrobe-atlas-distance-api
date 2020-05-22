from typing import Union

from py2neo import Graph, Subgraph
from py2neo.ogm import GraphObject


class Neo4jDriver:
    instance: Union['Neo4jDriver'] = None
    uri = 'bolt://localhost:7687'
    encrypted = False

    def __init__(self):
        self.graph = Graph(self.uri, secure=self.encrypted)

    def push(self, graph: Union[Subgraph, GraphObject]):
        self.graph.push(graph)

    def exists(self, graph: Union[Subgraph, GraphObject]) -> bool:
        return self.graph.exists(graph)

    @classmethod
    def get(cls) -> Union['Neo4jDriver']:
        if not cls.instance:
            cls.instance = Neo4jDriver()
        return cls.instance
