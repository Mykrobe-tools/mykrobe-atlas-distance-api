from flask import g

from swagger_server.models.sample import Sample  # noqa: E501


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample based on a sample ID. # noqa: E501

    :param id: 
    :type id: str

    :rtype: Sample
    """

    graph = g.db
    exp_id = graph.get_node_by_id(id)
    sample = Sample(exp_id)

    return sample.to_dict()
