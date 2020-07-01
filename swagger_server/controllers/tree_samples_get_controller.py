from swagger_server.db import get_db
from swagger_server.exceptions import NotFound
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.ogm.mappers import SampleNode, LeafNode


def tree_id_samples_get(id):  # noqa: E501
    """tree_id_samples_get

    Return the list of nearest samples of a tree node based on an ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: List[Neighbour]
    """

    sample_graph = get_db()

    try:
        nodes = LeafNode.get(id, sample_graph).samples
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return [x.to_model() for x in nodes], 200
