from hypothesis.strategies import composite, text, integers, characters

from swagger_server.models import Neighbour, Sample


def neo4j_strings():
    return text(characters(whitelist_categories=('L', 'N')))


def neo4j_integers():
    return integers(min_value=-2**63, max_value=2**63-1)


@composite
def samples(draw):
    experiment_id = draw(neo4j_strings())
    return Sample(experiment_id)


@composite
def neighbours(draw):
    experiment_id = draw(neo4j_strings())
    distance = draw(neo4j_integers())
    return Neighbour(experiment_id, distance)
