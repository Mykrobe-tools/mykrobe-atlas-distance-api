from neomodel import StructuredNode, StringProperty, Relationship, StructuredRel, IntegerProperty, RelationshipTo


class DistanceRel(StructuredRel):
    dist = IntegerProperty()


class SampleNode(StructuredNode):
    name = StringProperty()
    neighbors = Relationship('SampleNode', 'NEIGHBOR', model=DistanceRel)
    parent = RelationshipTo('SampleNode', 'PARENT')
