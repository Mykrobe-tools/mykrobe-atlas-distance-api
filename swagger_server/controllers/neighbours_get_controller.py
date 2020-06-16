from swagger_server import services
from swagger_server.exceptions import NotFound
from swagger_server.models.error import Error  # noqa: E501


def samples_id_nearest_neighbours_get(id):  # noqa: E501
    """samples_id_nearest_neighbours_get

    Return the list of nearest neighbours of a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: List[Neighbour]
    """

    try:
        resource = services.get_neighbours(id)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        if not resource:
            return Error(404, 'Not found'), 404
        return resource, 200
