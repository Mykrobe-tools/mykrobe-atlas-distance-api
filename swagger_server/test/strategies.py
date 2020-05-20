from hypothesis import strategies as st
from hypothesis.strategies import composite, integers, text, characters

from swagger_server.models import Neighbour


@composite
def neighbours(draw):
    experiment_id = draw(text(alphabet=characters(whitelist_categories=('L', 'N')), min_size=1))
    distance = draw(integers(max_value=2 ** 63 - 1, min_value=-2 ** 63))
    return Neighbour(experiment_id, distance)


experiment_id_st = st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1)