from py2neo import Graph

from swagger_server.exceptions import Exists, NotFound
from swagger_server.factories import SampleFactory
from swagger_server.models import Sample
from swagger_server.ogm import SampleNode, LeafNode


def create_sample(sample: Sample, graph: Graph) -> Sample:
    node = SampleNode()
    node.experiment_id = sample.experiment_id

    if node.exists(graph):
        raise Exists

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
    match = SampleNode.match(graph, experiment_id).limit(1)
    if len(match) == 0:
        raise NotFound
    return SampleFactory.build(match.first())


def delete_sample(experiment_id: str, graph: Graph):
    match = SampleNode.match(graph, experiment_id).limit(1)
    if len(match) == 0:
        raise NotFound
    graph.delete(match.first())
