from flask import g

from swagger_server.models import Error
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.services import graph
from swagger_server.services.graph import ObjectNotFound


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: Sample
    """

    db = g.db

    try:
        sample = graph.get_sample(id, db)
    except ObjectNotFound:
        return Error(404, 'Not found'), 404
    else:
        return sample
