from swagger_server.db import get_db
from swagger_server.exceptions import NotFound
from swagger_server.models import Error
from swagger_server.ogm.mappers import SampleNode


def samples_id_nearest_neighbours_get(id):  # noqa: E501
    """samples_id_nearest_neighbours_get

    Return the list of nearest neighbours of a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: List[Neighbour]
    """

    sample_graph = get_db()

    try:
        node = SampleNode.get(id, sample_graph)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        model = node.to_model()

        if not model.nearest_neighbours:
            return Error(404, 'Not found'), 404
        else:
            return node.to_model().nearest_neighbours, 200
