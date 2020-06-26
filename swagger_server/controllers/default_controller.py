import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.leaf import Leaf  # noqa: E501
from swagger_server.models.neighbour import Neighbour  # noqa: E501
from swagger_server import util


def tree_id_delete(id):  # noqa: E501
    """tree_id_delete

    Delete a leaf node based on an ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def tree_id_get(id):  # noqa: E501
    """tree_id_get

    Return the list of nearest samples of a tree node based on an ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: List[Neighbour]
    """
    return 'do some magic!'


def tree_post(leaf):  # noqa: E501
    """tree_post

    Create a leaf node for the phylogenetic tree. # noqa: E501

    :param leaf: Leaf node to be added
    :type leaf: dict | bytes

    :rtype: Leaf
    """
    if connexion.request.is_json:
        leaf = Leaf.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
