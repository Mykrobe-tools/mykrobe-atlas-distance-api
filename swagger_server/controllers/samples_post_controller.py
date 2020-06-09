import connexion
from flask import g

from swagger_server.models import Error
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.services import graph
from swagger_server.services.graph import ObjectExisted


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

    try:
        graph.create_sample(body, db)
    except ObjectExisted:
        return Error(409, 'Already existed'), 409
    else:
        return body, 201
