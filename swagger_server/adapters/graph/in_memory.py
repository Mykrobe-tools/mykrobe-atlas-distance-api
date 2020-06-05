import networkx

from swagger_server.adapters.graph.base import AbstractGraph


class InMemoryGraph(AbstractGraph):
    def __init__(self):
        self.graph = networkx.Graph()

    def add_node(self, **attributes):
        key = InMemoryGraph._key_from_attributes(attributes)
        self.graph.add_node(key, **attributes)

    def get_node(self, **attributes):
        key = InMemoryGraph._key_from_attributes(attributes)
        return self.graph.nodes[key]

    @staticmethod
    def _key_from_attributes(attributes):
        return '_'.join([str(v) for v in attributes.values()])