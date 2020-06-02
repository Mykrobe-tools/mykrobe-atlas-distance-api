from py2neo.ogm import GraphObject, Property


class SampleNode(GraphObject):
    __primarylabel__ = 'SampleNode'
    __primarykey__ = 'name'  # NOTE: This does not enforce unique constraint, but only assist in querying

    name = Property()
