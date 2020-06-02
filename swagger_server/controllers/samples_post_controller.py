import connexion

from swagger_server import services
from swagger_server.adapters.repositories.sample_repository import SampleAlreadyExist
from swagger_server.databases.neo4j import Neo4jDatabase
from swagger_server.models import Error
from swagger_server.models.sample import Sample  # noqa: E501


def samples_post(body):  # noqa: E501
    """samples_post

    Add a new sample. Duplicates are not allowed # noqa: E501

    :param body: Sample to be added
    :type body: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        body = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    db = Neo4jDatabase()

    try:
        services.add_new_sample(body, db)
    except SampleAlreadyExist:
        return Error(409, 'Already existed'), 409
    else:
        return body, 201
