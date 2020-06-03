from typing import Any

from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

NEIGHBOUR_REL_TYPE = 'NEIGHBOUR'
LINEAGE_REL_TYPE = 'LINEAGE'


class BaseGraphObject(GraphObject):
    @classmethod
    def primary_key_exists(cls, primary_value: Any, graph: Graph) -> bool:
        kwargs = {
            cls.__primarykey__: primary_value
        }
        return len(cls.match(graph).where(**kwargs)) > 0


class LeafNode(BaseGraphObject):
    __primarykey__ = 'name'

    name = Property()


class SampleNode(BaseGraphObject):
    __primarykey__ = 'name'

    name = Property()

    neighbours = RelatedTo('SampleNode', NEIGHBOUR_REL_TYPE)
    lineage = RelatedTo(LeafNode, LINEAGE_REL_TYPE)
