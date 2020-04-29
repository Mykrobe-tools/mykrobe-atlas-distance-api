import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.leaf import Leaf  # noqa: E501
from swagger_server.models.nearest_leaf import NearestLeaf  # noqa: E501
from swagger_server.models.neighbour import Neighbour  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server import util


def samples_id_delete(id):  # noqa: E501
    """samples_id_delete

    Delete a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: Sample
    """
    return 'do some magic!'


def samples_id_nearest_leaf_node_put(body, id):  # noqa: E501
    """samples_id_nearest_leaf_node_put

    Replace the nearest leaf node of a sample based on a sample ID. # noqa: E501

    :param body: New nearest leaf node to replace old one.
    :type body: dict | bytes
    :param id: 
    :type id: str

    :rtype: NearestLeaf
    """
    if connexion.request.is_json:
        body = NearestLeaf.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def samples_id_nearest_neighbours_put(body, id):  # noqa: E501
    """samples_id_nearest_neighbours_put

    Replace the list of nearest neighbours of a sample based on a sample ID. # noqa: E501

    :param body: New list of nearest neighbours to replace old one.
    :type body: list | bytes
    :param id: 
    :type id: str

    :rtype: List[Neighbour]
    """
    if connexion.request.is_json:
        body = [Neighbour.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


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


def tree_post(body):  # noqa: E501
    """tree_post

    Create a leaf node for the phylogenetic tree. # noqa: E501

    :param body: Leaf node to be added
    :type body: dict | bytes

    :rtype: Leaf
    """
    if connexion.request.is_json:
        body = Leaf.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
