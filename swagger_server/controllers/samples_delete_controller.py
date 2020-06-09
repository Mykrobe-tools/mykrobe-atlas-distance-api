import connexion
import six
from flask import g

from swagger_server.models.error import Error  # noqa: E501
from swagger_server import util
from swagger_server.services import graph
from swagger_server.services.graph import ObjectNotFound


def samples_id_delete(id):  # noqa: E501
    """samples_id_delete

    Delete a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: None
    """

    db = g.db

    try:
        graph.delete_sample(id, db)
    except ObjectNotFound:
        return Error(404, 'Not found'), 404
    else:
        return {}, 200
