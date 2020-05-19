from swagger_server.helpers import db
from swagger_server.helpers.controller_helpers import handle_500
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501


@handle_500
def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: Sample
    """

    rows = db.Neo4jDatabase.get().query(f'MATCH (n:SampleNode {{name: "{id}"}}) RETURN n').values()

    if not rows:
        return Error(404, 'Not found'), 404

    return Sample(rows[0][0]['name']), 200
