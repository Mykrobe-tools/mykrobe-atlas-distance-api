import connexion

from swagger_server.db import get_db
from swagger_server.exceptions import AlreadyExisted
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.leaf import Leaf  # noqa: E501
from swagger_server.ogm.leaf_node import LeafNode


def tree_post(leaf=None):  # noqa: E501
    """tree_post

    Create a leaf node for the phylogenetic tree. # noqa: E501

    :param leaf: Leaf node to be added
    :type leaf: dict | bytes

    :rtype: Leaf
    """
    if connexion.request.is_json:
        leaf = Leaf.from_dict(connexion.request.get_json())  # noqa: E501

    sample_graph = get_db()

    try:
        node = LeafNode.create(leaf, sample_graph)
    except AlreadyExisted:
        return Error(409, 'Already existed'), 409
    else:
        return node.to_model(), 201
