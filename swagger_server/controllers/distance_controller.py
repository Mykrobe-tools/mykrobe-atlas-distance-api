from flask import current_app

from swagger_server.helpers import db
from swagger_server.helpers.controller_helpers import handle_500
from swagger_server.models import Neighbour
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.nearest_leaf import NearestLeaf  # noqa: E501


@handle_500
def samples_id_nearest_leaf_node_get(id):  # noqa: E501
    """samples_id_nearest_leaf_node_get

    Return the nearest leaf node of a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: NearestLeaf
    """

    result = db.Database.get().query(f'MATCH (n:SampleNode)-[r:LINEAGE]->(m:LineageNode) WHERE n.name="{id}" RETURN '
                                     f'n,r,m').values()

    if not result:
        if current_app.config['DEBUG']:
            current_app.logger.debug({'error': 'empty result', 'method': samples_id_nearest_leaf_node_get.__name__,
                                      'id': id, 'result': result})
        return Error(404, "Not found"), 404

    rel = result[0][1]
    leaf = result[0][2]

    resp = NearestLeaf(leaf['name'], distance=rel['dist'])
    return resp, 200


@handle_500
def samples_id_nearest_neighbours_get(id):  # noqa: E501
    """samples_id_nearest_neighbours_get

    Return the list of nearest neighbours of a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: List[Neighbour]
    """

    result = db.Database.get().query(
        f'MATCH (n:SampleNode {{name: "{id}"}}) OPTIONAL MATCH (n)-[r:NEIGHBOUR]-(m:SampleNode) RETURN '
        f'n,r,m').values()

    if not result:
        if current_app.config['DEBUG']:
            current_app.logger.debug({'error': 'empty result', 'method': samples_id_nearest_neighbours_get.__name__,
                                     'id': id, 'result': result})
        return Error(404, "Not found"), 404

    rels = [r[1] for r in result if r[1]]
    neighbors = [r[2] for r in result if r[2]]

    resp = [Neighbour(neighbors[i]['name'], distance=rels[i]['dist']) for i in range(len(neighbors))]
    return resp, 200
