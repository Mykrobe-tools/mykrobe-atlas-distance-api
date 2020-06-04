import networkx

from swagger_server.adapters.graph.base import AbstractGraph, NodeNotFound


class InMemoryGraph(AbstractGraph):
    def __init__(self):
        self.graph = networkx.Graph()

    def add_node(self, node):
        self.graph.add_node(node)

    def get_node_by_id(self, id_):
        for node in self.graph.nodes:
            if node == id_:
                return node

        raise NodeNotFound