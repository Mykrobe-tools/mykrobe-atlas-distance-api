from hypothesis.strategies import composite, text, integers, characters

from swagger_server.models import Neighbour, Sample


def experiment_ids():
    return text(characters(whitelist_categories=('L', 'N')))


def distances():
    return integers(min_value=-2**63, max_value=2**63-1)


@composite
def samples(draw):
    experiment_id = draw(experiment_ids())
    return Sample(experiment_id)


@composite
def neighbours(draw):
    experiment_id = draw(experiment_ids())
    distance = draw(distances())
    return Neighbour(experiment_id, distance)
