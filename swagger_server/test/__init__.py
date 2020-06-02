from hypothesis.strategies import register_type_strategy

from swagger_server.models import NearestLeaf, Neighbour, Sample
from swagger_server.test.strategies import nearest_leafs, neighbours, samples

register_type_strategy(NearestLeaf, nearest_leafs())
register_type_strategy(Neighbour, neighbours())
register_type_strategy(Sample, samples())
