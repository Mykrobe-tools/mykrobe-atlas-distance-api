from py2neo.ogm import GraphObject, Property, RelatedTo


class LeafNode(GraphObject):
    __primarylabel__ = 'LineageNode'
    __primarykey__ = 'name'

    name = Property()


class SampleNode(GraphObject):
    __primarylabel__ = 'SampleNode'
    __primarykey__ = 'name'  # NOTE: This does not enforce unique constraint, but only assist in querying

    name = Property()

    neighbours = RelatedTo('SampleNode', 'NEIGHBOUR')
    lineage = RelatedTo(LeafNode, 'LINEAGE')
