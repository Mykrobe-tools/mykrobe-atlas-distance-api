import connexion

from swagger_server.db import get_db
from swagger_server.exceptions import NotFound
from swagger_server.models import Error
from swagger_server.models.nearest_leaf import NearestLeaf  # noqa: E501
from swagger_server.ogm.mappers import SampleNode


def samples_id_nearest_leaf_node_put(id, nearest_leaf=None):  # noqa: E501
    """samples_id_nearest_leaf_node_put

    Replace the nearest leaf node of a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str
    :param nearest_leaf: New nearest leaf node to replace old one.
    :type nearest_leaf: dict | bytes

    :rtype: NearestLeaf
    """
    if connexion.request.is_json:
        nearest_leaf = NearestLeaf.from_dict(connexion.request.get_json())  # noqa: E501

    sample_graph = get_db()

    try:
        updated = SampleNode.update(id, sample_graph, leaf=nearest_leaf)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return updated.to_model().nearest_leaf_node, 200
