from hypothesis.strategies import register_type_strategy

from swagger_server.models import Neighbour
from swagger_server.test.strategies import neighbours

register_type_strategy(Neighbour, neighbours())
