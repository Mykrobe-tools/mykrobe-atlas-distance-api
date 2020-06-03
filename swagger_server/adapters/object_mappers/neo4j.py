from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

from swagger_server.models import Sample


class LeafNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()


class SampleNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')

    @classmethod
    def exists(cls, sample: Sample, graph: Graph) -> bool:
        sample_names = [sample.experiment_id]
        if sample.nearest_neighbours:
            sample_names += [n.experiment_id for n in sample.nearest_neighbours]

        return len(cls.match(graph).where(f'_.{cls.__primarykey__} IN {sample_names}')) > 0
