from py2neo.ogm import GraphObject, Property

from swagger_server.models import Sample


class SampleNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()

    def __init__(self, sample: Sample = None, name: str = None):
        if sample:
            self.name = sample.experiment_id
        elif name is not None:
            self.name = name
        else:
            raise AssertionError('either "sample" or "name" argument must be filled')
