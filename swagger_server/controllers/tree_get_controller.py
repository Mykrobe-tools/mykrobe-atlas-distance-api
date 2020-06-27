import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.neighbour import Neighbour  # noqa: E501
from swagger_server import util


def tree_id_get(id):  # noqa: E501
    """tree_id_get

    Return the list of nearest samples of a tree node based on an ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: List[Neighbour]
    """
    return 'do some magic!'
