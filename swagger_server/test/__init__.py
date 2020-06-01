from hypothesis.strategies import register_type_strategy

from swagger_server.models import Sample
from swagger_server.test.strategies import samples

register_type_strategy(Sample, samples())
