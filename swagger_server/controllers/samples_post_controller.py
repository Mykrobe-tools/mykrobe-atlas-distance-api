import connexion
from flask import g

from swagger_server.factories import SampleFactory
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.ogm import SampleNode, LeafNode


def samples_post(sample=None):  # noqa: E501
    """samples_post

    Add a new sample. Duplicates are not allowed # noqa: E501

    :param sample: Sample to be added
    :type sample: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        sample = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    sample_graph = g.sample_graph

    node = SampleNode()
    node.experiment_id = sample.experiment_id

    if sample.nearest_leaf_node:
        n = LeafNode()
        n.leaf_id = sample.nearest_leaf_node.leaf_id
        if n.exists(sample_graph):
            node.lineage.add(n, distance=sample.nearest_leaf_node.distance)

    if sample.nearest_neighbours:
        for neighbour in sample.nearest_neighbours:
            if neighbour.experiment_id != sample.experiment_id:
                n = SampleNode()
                n.experiment_id = neighbour.experiment_id
                if n.exists(sample_graph):
                    node.neighbours.add(n, distance=neighbour.distance)

    if node.exists(sample_graph):
        return Error(409, 'Already existed'), 409
    sample_graph.push(node)

    return SampleFactory.build(node), 201
