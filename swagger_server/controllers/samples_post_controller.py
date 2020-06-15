import connexion

from swagger_server import registry
from swagger_server.exceptions import Exists
from swagger_server.factories import GraphFactory
from swagger_server.models import Error
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.repositories import Neo4jRepository


def samples_post(body):  # noqa: E501
    """samples_post

    Add a new sample. Duplicates are not allowed # noqa: E501

    :param body: Sample to be added
    :type body: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        body = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    db = registry.get('db')

    try:
        node = GraphFactory.build(body)
        db.create(node)
    except Exists:
        return Error(409, 'Already existed'), 409
    else:
        return body, 201
