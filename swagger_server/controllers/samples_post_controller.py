import connexion
from flask import g

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

    graph = g.db
    graph.add_node(body.experiment_id)

    return body, 201
