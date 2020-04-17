import connexion

from swagger_server.models import ApiResponse
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.orm.DistanceORM import SampleNode


def distance_post(body):  # noqa: E501
    """distance_post

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        sample = Sample.from_dict(connexion.request.get_json())  # noqa: E501

        neighbors = SampleNode.nodes.filter(name=sample.experiment_id)\
            .neighbors.match(dist__lt=10)

        return ApiResponse(
            type='distance',
            sub_type='nearest-neighbor',
            result=[{
                'name': s.name
            } for s in neighbors]
        )
