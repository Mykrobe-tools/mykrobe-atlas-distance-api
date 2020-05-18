from flask import current_app

from swagger_server.dal import get_nearest_neighbours, get_nearest_leaf_node
from swagger_server.models import Neighbour
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.nearest_leaf import NearestLeaf  # noqa: E501


def samples_id_nearest_leaf_node_get(id):  # noqa: E501
    """samples_id_nearest_leaf_node_get

    Return the nearest leaf node of a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: NearestLeaf
    """

    try:
        result = get_nearest_leaf_node(id)

        if not result:
            return Error(404, "Not found"), 404

        resp = NearestLeaf(result['leaf_id'], distance=result['distance'])
        return resp, 200
    except BaseException as e:
        current_app.logger.error(e)
        return Error(500, "Unexpected error"), 500


def samples_id_nearest_neighbours_get(id):  # noqa: E501
    """samples_id_nearest_neighbours_get

    Return the list of nearest neighbours of a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: List[Neighbour]
    """

    try:
        result = get_nearest_neighbours(id)

        if not result:
            return Error(404, "Not found"), 404

        resp = [Neighbour(r['experiment_id'], r['distance']) for r in result]
        return resp, 200
    except BaseException as e:
        current_app.logger.error(e)
        return Error(500, "Unexpected error"), 500
