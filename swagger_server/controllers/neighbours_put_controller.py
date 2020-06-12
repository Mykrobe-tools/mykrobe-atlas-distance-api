import connexion

from swagger_server.exceptions import NotFound
from swagger_server.factories import GraphFactory
from swagger_server.models import Sample
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.neighbour import Neighbour  # noqa: E501
from swagger_server.repositories import Neo4jRepository


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

    db = Neo4jRepository()

    try:
        sample = Sample(id, body)
        node = GraphFactory.build(sample)
        db.update(node)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return body, 200
