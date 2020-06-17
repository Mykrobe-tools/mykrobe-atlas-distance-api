import connexion

from swagger_server import services
from swagger_server.exceptions import NotFound
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.neighbour import Neighbour  # noqa: E501


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

    try:
        updated = services.update_neighbours(id, body)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return updated, 200
