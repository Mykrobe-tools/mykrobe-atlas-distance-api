from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.models import Leaf, Sample
from swagger_server.ogm.base import GraphModel


class LeafNode(GraphObject):
    __primarylabel__ = Leaf.__name__
    __primarykey__ = 'leaf_id'

    leaf_id = Property()


class SampleNode(GraphModel):
    __primarylabel__ = Sample.__name__
    __primarykey__ = 'experiment_id'

    experiment_id = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')
