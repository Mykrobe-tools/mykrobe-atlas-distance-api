from py2neo import Graph

from swagger_server.adapters.ogm.neo4j import SampleNode
from swagger_server.models import Sample


class SampleRepository:
    def __init__(self, graph: Graph):
        self.graph = graph

    def add(self, sample: Sample):
        node = SampleNode()
        node.name = sample.experiment_id

        self.graph.create(node)
