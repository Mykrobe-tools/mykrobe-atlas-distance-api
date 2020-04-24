from neomodel import StructuredNode, StringProperty, Relationship, StructuredRel, IntegerProperty, RelationshipTo


class DistanceRel(StructuredRel):
    dist = IntegerProperty()


class SampleNode(StructuredNode):
    name = StringProperty()
    neighbors = Relationship('SampleNode', 'NEIGHBOR', model=DistanceRel)
    lineage = RelationshipTo('LineageNode', 'LINEAGE', model=DistanceRel)


class LineageNode(StructuredNode):
    name = StringProperty()
