from swagger_server.db import get_db
from swagger_server.exceptions import NotFound
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.ogm.leaf_node import LeafNode


def tree_id_get(id):  # noqa: E501
    """tree_id_get

    Return a tree node based on an ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: Leaf
    """

    sample_graph = get_db()

    try:
        node = LeafNode.get(id, sample_graph)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return node.to_model(), 200
