import connexion
from flask import g

from swagger_server.exceptions import Existed
from swagger_server.factories import SampleFactory
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.services import create_sample


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

    try:
        node = create_sample(sample, sample_graph)
    except Existed:
        return Error(409, 'Already existed'), 409
    else:
        return SampleFactory.build(node), 201
