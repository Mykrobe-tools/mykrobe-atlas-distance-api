from flask import g

from swagger_server.exceptions import NotFound
from swagger_server.factories import SampleFactory
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.services import get_sample


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: Sample
    """

    sample_graph = g.sample_graph

    try:
        node = get_sample(id, sample_graph)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return SampleFactory.build(node), 200
