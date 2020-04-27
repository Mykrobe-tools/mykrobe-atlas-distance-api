from flask import current_app

from swagger_server.models import Neighbour
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.nearest_leaf import NearestLeaf  # noqa: E501
from swagger_server.orm.DistanceORM import SampleNode, LineageNode


def samples_id_nearest_leaf_node_get(id):  # noqa: E501
    """samples_id_nearest_leaf_node_get

    Return the nearest leaf node of a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: NearestLeaf
    """

    try:
        node = SampleNode.nodes.get(name=id)
        leaf = node.lineage.get()
        rel = node.lineage.relationship(leaf)

        resp = NearestLeaf(leaf.name, distance=rel.dist)

        return resp, 200
    except (SampleNode.DoesNotExist, LineageNode.DoesNotExist) as e:
        current_app.logger.error(e)
        return Error(404, "Not found"), 404
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
        node = SampleNode.nodes.get(name=id)
        neighbors = node.neighbors.all()
        rels = [node.neighbors.relationship(n) for n in neighbors]

        resp = [Neighbour(neighbors[i].name, distance=rels[i].dist) for i in range(len(neighbors))]

        return resp, 200
    except SampleNode.DoesNotExist as e:
        current_app.logger.error(e)
        return Error(404, "Not found"), 404
    except BaseException as e:
        current_app.logger.error(e)
        return Error(500, "Unexpected error"), 500
