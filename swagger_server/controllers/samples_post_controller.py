import connexion

from swagger_server.db import get_db
from swagger_server.exceptions import AlreadyExisted
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.ogm.sample_node import SampleNode
from swagger_server.validators import SampleValidator


def samples_post(sample=None):  # noqa: E501
    """samples_post

    Add a new sample. Duplicates are not allowed # noqa: E501

    :param sample: Sample to be added
    :type sample: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        sample = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    valid, error = SampleValidator(sample).valid()
    if not valid:
        return Error(400, error), 400

    sample_graph = get_db()

    try:
        node = SampleNode.create(sample, sample_graph)
    except AlreadyExisted:
        return Error(409, 'Already existed'), 409
    else:
        return node.to_model(), 201
