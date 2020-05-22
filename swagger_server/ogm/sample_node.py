from py2neo.ogm import GraphObject, Property


class SampleNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()
