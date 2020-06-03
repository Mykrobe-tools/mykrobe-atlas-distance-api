from py2neo.ogm import GraphObject, Property, RelatedTo


class LeafNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()


class SampleNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')
