import connexion

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.services import SampleManagementService
from swagger_server.services.sample_management import DuplicatedSample


def samples_post(body):  # noqa: E501
    """samples_post

    Add a new sample. Duplicates are not allowed # noqa: E501

    :param body: Sample to be added
    :type body: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        body = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    try:
        SampleManagementService.add(body)
        return body, 201
    except DuplicatedSample:
        return Error(409, 'Already existed'), 409
