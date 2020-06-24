from py2neo import Graph
from py2neo.ogm import RelatedObjects

from swagger_server.exceptions import AlreadyExisted, NotFound
from swagger_server.models import Sample
from swagger_server.ogm import SampleNode, LeafNode


def create_sample(sample: Sample, graph: Graph) -> SampleNode:
    node = SampleNode()
    node.experiment_id = sample.experiment_id

    if node.exists(graph):
        raise AlreadyExisted

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

    return node


def get_sample(experiment_id: str, graph: Graph) -> SampleNode:
    match = SampleNode.match(graph, experiment_id).limit(1)
    if len(match) == 0:
        raise NotFound
    return match.first()


def delete_sample(experiment_id: str, graph: Graph):
    graph.delete(get_sample(experiment_id, graph))


def get_neighbours(experiment_id: str, graph: Graph) -> RelatedObjects:
    return get_sample(experiment_id, graph).neighbours
