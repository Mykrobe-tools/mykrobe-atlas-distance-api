from flask import g

from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.services import graph


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: Sample
    """

    db = g.db

    sample = graph.get_sample(id, db)

    return sample
