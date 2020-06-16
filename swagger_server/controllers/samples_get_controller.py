from swagger_server import services
from swagger_server.exceptions import NotFound
from swagger_server.models import Error
from swagger_server.models.sample import Sample  # noqa: E501


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample based on a sample ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: Sample
    """

    try:
        resource = services.get_sample(id)
    except NotFound:
        return Error(404, 'Not found'), 404
    else:
        return resource, 200
