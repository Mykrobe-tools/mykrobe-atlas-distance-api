from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.models import Sample


NEIGHBOUR_REL_TYPE = 'NEIGHBOUR'
LINEAGE_REL_TYPE = 'LINEAGE'


class LeafNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()


class SampleNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()

    neighbours = RelatedTo('SampleNode', NEIGHBOUR_REL_TYPE)
    lineage = RelatedTo(LeafNode, LINEAGE_REL_TYPE)

    @classmethod
    def exists(cls, sample: Sample, graph: Graph) -> bool:
        return len(cls.match(graph).where(name=sample.experiment_id)) > 0
