import connexion
from neomodel import db

from swagger_server.models import ApiResponse
from swagger_server.models.sample import Sample  # noqa: E501


def distance_post(body):  # noqa: E501
    """distance_post

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        sample = Sample.from_dict(connexion.request.get_json())  # noqa: E501

        if sample.sub_type == 'nearest-neighbor':
            results, _ = db.cypher_query(
                'MATCH (a:SampleNode)-[n:NEIGHBOR]-(b:SampleNode) '
                'WHERE a.name={sample_name} AND n.dist < 10 '
                'RETURN b, n.dist',
                {'sample_name': sample.experiment_id}
            )
            api_result = {r[0]['name']: r[1] for r in results}
        elif sample.sub_type == 'nearest-leaf-node':
            results, _ = db.cypher_query(
                'MATCH (a:SampleNode)<-[n:PARENT]-(b:SampleNode) '
                'WHERE a.name={sample_name} '
                'RETURN b',
                {'sample_name': sample.experiment_id}
            )
            api_result = {r[0]['name']: '' for r in results}
        else:
            return 'Invalid sub_type', 400

        return ApiResponse(
            type='distance',
            sub_type=sample.sub_type,
            result=api_result
        )
