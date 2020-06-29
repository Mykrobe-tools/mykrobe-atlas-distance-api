import connexion

from swagger_server.db import get_db
from swagger_server.exceptions import NotFound
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.neighbour import Neighbour  # noqa: E501
from swagger_server.ogm.sample_node import SampleNode


def samples_id_nearest_neighbours_put(id, neighbour=None):  # noqa: E501
    """samples_id_nearest_neighbours_put

    Replace the list of nearest neighbours of a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str
    :param neighbour: New list of nearest neighbours to replace old one.
    :type neighbour: list | bytes

    :rtype: List[Neighbour]
    """
    if connexion.request.is_json:
        neighbour = [Neighbour.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501

    sample_graph = get_db()

    try:
        updated = SampleNode.update(id, sample_graph, neighbours=neighbour)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return updated.to_model().nearest_neighbours, 200
