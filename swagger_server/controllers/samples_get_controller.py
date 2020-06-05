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
    node = graph.get_node(label=Sample.__name__, experiment_id=id)

    sample = Sample(node['experiment_id'])
    return sample.to_dict()
