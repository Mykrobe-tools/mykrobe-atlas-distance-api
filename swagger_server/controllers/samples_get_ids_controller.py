import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server import util


def samples_get(ids=None):  # noqa: E501
    """samples_get

    Return one or more samples based on IDs # noqa: E501

    :param ids: A comma-separated list of sample IDs
    :type ids: List[str]

    :rtype: List[Sample]
    """
    return 'do some magic!'
