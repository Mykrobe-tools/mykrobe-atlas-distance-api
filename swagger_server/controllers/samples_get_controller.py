from flask import g

from swagger_server.factories import SampleFactory
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.ogm import SampleNode


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: Sample
    """

    sample_graph = g.sample_graph

    samples = SampleNode.match(sample_graph, id)

    if len(samples) == 0:
        return Error(404, 'Not found'), 404
    else:
        return SampleFactory.build(samples.first())
