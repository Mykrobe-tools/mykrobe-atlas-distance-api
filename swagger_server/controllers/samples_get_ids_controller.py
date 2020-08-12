from swagger_server.db import get_db
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.ogm.mappers import SampleNode


def samples_get(ids=None):  # noqa: E501
    """samples_get

    Return one or more samples based on IDs # noqa: E501

    :param ids: A comma-separated list of sample IDs
    :type ids: List[str]

    :rtype: List[Sample]
    """

    sample_graph = get_db()

    samples = list(map(lambda x: x.to_model(),
                       SampleNode.match(sample_graph).where("_.experiment_id =~ '{}'".format('|'.join(ids)))))

    if samples:
        return samples, 200

    return Error(404, 'Not found'), 404
