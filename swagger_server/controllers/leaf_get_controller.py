from flask import g

from swagger_server.exceptions import NotFound
from swagger_server.factories import NearestLeafFactory
from swagger_server.models import Error
from swagger_server.models.nearest_leaf import NearestLeaf  # noqa: E501
from swagger_server.services import get_nearest_leaf


def samples_id_nearest_leaf_node_get(id):  # noqa: E501
    """samples_id_nearest_leaf_node_get

    Return the nearest leaf node of a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: NearestLeaf
    """

    sample_graph = g.sample_graph

    try:
        relationship = get_nearest_leaf(id, sample_graph)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return NearestLeafFactory.build(relationship)
