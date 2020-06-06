import connexion
from flask import g
from py2neo import Node

from swagger_server.models import Error
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.services import graph


def samples_post(body):  # noqa: E501
    """samples_post

    Add a new sample. Duplicates are not allowed # noqa: E501

    :param body: Sample to be added
    :type body: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        body = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    db = g.db

    existing_node = db.nodes.match(Sample.__name__, experiment_id=body.experiment_id)
    if len(existing_node) > 0:
        return Error(409, 'Already existed'), 409

    subgraph = graph.build_graph(body)
    db.create(subgraph)

    return body, 201
