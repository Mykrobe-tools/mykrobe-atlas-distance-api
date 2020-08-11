from swagger_server.db import get_db
from swagger_server.exceptions import NotFound
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

    samples = []
    for sample_id in ids:
        try:
            node = SampleNode.get(sample_id, sample_graph)
        except NotFound:
            pass
        else:
            samples.append(node.to_model())

    if samples:
        return samples, 200

    return Error(404, 'Not found'), 404
