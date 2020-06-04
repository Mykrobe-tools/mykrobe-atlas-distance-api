import py2neo
from py2neo import Node

from swagger_server.adapters.graph.base import AbstractGraph, NodeNotFound


class PersistentGraph(AbstractGraph):
    def __init__(self):
        self.graph = py2neo.Graph()

    def add_node(self, node):
        node = Node(name=node)
        self.graph.create(node)

    def get_node_by_id(self, id_):
        nodes = self.graph.nodes.match(name=id_)
        for node in nodes:
            return node['name']

        raise NodeNotFound
