import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.neighbour import Neighbour  # noqa: E501
from swagger_server import util


def samples_id_nearest_neighbours_get(id):  # noqa: E501
    """samples_id_nearest_neighbours_get

    Return the list of nearest neighbours of a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: List[Neighbour]
    """
    return 'do some magic!'
