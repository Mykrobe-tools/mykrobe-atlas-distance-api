import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server import util


def samples_post():  # noqa: E501
    """samples_post

    Add a new sample. Duplicates are not allowed # noqa: E501

    :param sample: Sample to be added
    :type sample: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        sample = Sample.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
