from flask import g

from swagger_server.exceptions import NotFound
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.ogm.mappers import SampleNode


def samples_id_delete(id):  # noqa: E501
    """samples_id_delete

    Delete a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: None
    """

    db = g.db

    try:
        SampleNode.delete(id, db)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return {}, 200
