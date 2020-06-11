from flask import g

from swagger_server.exceptions import NotFound
from swagger_server.factories import ModelFactory
from swagger_server.models import Error
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.ogm import SampleNode


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: Sample
    """

    db = g.db

    try:
        sample_node = SampleNode.get(id, db)
        sample = ModelFactory.build(sample_node)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return sample
