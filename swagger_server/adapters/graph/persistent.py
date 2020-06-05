import py2neo
from py2neo import Node

from swagger_server.adapters.graph.base import AbstractGraph


class PersistentGraph(AbstractGraph):
    def __init__(self):
        self.graph = py2neo.Graph()

    def add_node(self, **attributes):
        labels, attributes = PersistentGraph._extract_labels_from_attributes(attributes)
        node = Node(*labels, **attributes)

        self.graph.create(node)

    def get_node(self, **attributes):
        labels, attributes = PersistentGraph._extract_labels_from_attributes(attributes)
        return self.graph.nodes.match(*labels, **attributes).limit(1).first()

    @staticmethod
    def _extract_labels_from_attributes(attributes):
        label_key = 'label'
        labels_key = 'labels'
        assert (label_key in attributes) != (
                    labels_key in attributes), f'only either "{label_key}" or "{labels_key}" must be set'

        if label_key in attributes:
            labels = [attributes[label_key]]
            del attributes[label_key]
        else:
            labels = attributes[labels_key]
            del attributes[labels_key]

        return labels, attributes
