from py2neo import Graph

from swagger_server.exceptions import Existed
from swagger_server.factories import SampleFactory
from swagger_server.models import Sample
from swagger_server.ogm import SampleNode, LeafNode


def create_sample(sample: Sample, graph: Graph) -> Sample:
    node = SampleNode()
    node.experiment_id = sample.experiment_id

    if node.exists(graph):
        raise Existed

    if sample.nearest_leaf_node:
        n = LeafNode()
        n.leaf_id = sample.nearest_leaf_node.leaf_id
        if n.exists(graph):
            node.lineage.add(n, distance=sample.nearest_leaf_node.distance)

    if sample.nearest_neighbours:
        for neighbour in sample.nearest_neighbours:
            n = SampleNode()
            n.experiment_id = neighbour.experiment_id
            if n.exists(graph):
                node.neighbours.add(n, distance=neighbour.distance)

    graph.push(node)

    return SampleFactory.build(node)


def get_sample(experiment_id: str, graph: Graph) -> Sample:
    node = SampleNode.get(experiment_id, graph)
    return SampleFactory.build(node)
