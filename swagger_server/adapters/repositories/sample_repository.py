from py2neo import Graph, Node

from swagger_server.models import Sample


class SampleRepository:
    def __init__(self, graph: Graph):
        self.graph = graph

    def add(self, sample: Sample):
        self.graph.create(Node('SampleNode', name=sample.experiment_id))
