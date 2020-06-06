import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server import util


def samples_id_delete(id):  # noqa: E501
    """samples_id_delete

    Delete a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return Error(404, 'Not found'), 404
