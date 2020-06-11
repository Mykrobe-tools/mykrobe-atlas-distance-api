from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.ogm.base import GraphModel


class LeafNode(GraphObject):
    __primarykey__ = 'leaf_id'

    leaf_id = Property()


class SampleNode(GraphModel):
    __primarykey__ = 'experiment_id'

    experiment_id = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')
