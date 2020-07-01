from swagger_server.db import get_db
from swagger_server.exceptions import NotFound
from swagger_server.models import Error
from swagger_server.ogm.mappers import SampleNode


def samples_id_delete(id):  # noqa: E501
    """samples_id_delete

    Delete a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: None
    """

    sample_graph = get_db()

    try:
        SampleNode.delete(id, sample_graph)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return '', 204
