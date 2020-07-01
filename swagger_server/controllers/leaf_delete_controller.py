from swagger_server.db import get_db
from swagger_server.exceptions import NotFound
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.ogm.mappers import SampleNode


def samples_id_nearest_leaf_node_delete(id):  # noqa: E501
    """samples_id_nearest_leaf_node_delete

    Delete the nearest leaf node associated with a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: None
    """

    sample_graph = get_db()

    try:
        node = SampleNode.get(id, sample_graph)
        node.detach_lineage(sample_graph)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return '', 204
