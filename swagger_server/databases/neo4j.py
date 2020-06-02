from py2neo import Graph, NodeMatcher, ClientError
from py2neo.ogm import GraphObject

from swagger_server.databases.base import BaseDatabase
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

    def truncate(self):
        self.graph.delete_all()
