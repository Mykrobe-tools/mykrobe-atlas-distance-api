from swagger_server.dal.sample import delete_sample, SampleNotExist
from swagger_server.helpers import db
from swagger_server.helpers.controller_helpers import handle_500
from swagger_server.models.error import Error  # noqa: E501


@handle_500
def samples_id_delete(id):  # noqa: E501
    """samples_id_delete

    Delete a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """

    try:
        delete_sample(id)
        return '', 204
    except SampleNotExist:
        return Error(404, 'Not found'), 404
