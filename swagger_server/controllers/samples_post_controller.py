import connexion
from flask import g

from swagger_server.factories import SampleFactory, SampleNodeFactory
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

    node = SampleNodeFactory.build(sample, sample_graph)

    if node.exists(sample_graph):
        return Error(409, 'Already existed'), 409
    sample_graph.push(node)

    return SampleFactory.build(node), 201
