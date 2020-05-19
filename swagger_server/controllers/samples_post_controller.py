import connexion
from neobolt.exceptions import ConstraintError

from swagger_server.dal.sample import SampleAlreadyExist, create_sample
from swagger_server.helpers import db
from swagger_server.helpers.controller_helpers import handle_500
from swagger_server.models import Neighbour, NearestLeaf, Error
from swagger_server.models.sample import Sample  # noqa: E501


@handle_500
def samples_post(body):  # noqa: E501
    """samples_post

    Add a new sample. Duplicates are not allowed # noqa: E501

    :param body: Sample to be added
    :type body: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        sample = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    try:
        return create_sample(sample), 201
    except SampleAlreadyExist:
        return Error(409, 'Already existed'), 409
