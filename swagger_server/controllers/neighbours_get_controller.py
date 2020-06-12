from flask import g

from swagger_server.exceptions import NotFound
from swagger_server.factories import ModelFactory
from swagger_server.models import Sample
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.ogm import SampleNode


def samples_id_nearest_neighbours_get(id):  # noqa: E501
    """samples_id_nearest_neighbours_get

    Return the list of nearest neighbours of a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: List[Neighbour]
    """

    db = g.db

    try:
        sample_node = db.get(SampleNode, id)
        sample = ModelFactory.build(sample_node)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        if not sample.nearest_neighbours:
            return Error(404, 'Not found'), 404
        return sample
