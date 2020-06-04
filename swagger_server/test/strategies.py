from hypothesis.strategies import composite, text, integers, characters

from swagger_server.models import Sample, Neighbour, NearestLeaf


def safe_non_empty_strings():
    return text(alphabet=characters(whitelist_categories=('L', 'N')), min_size=1)


def neo4j_integers():
    return integers(min_value=-2**63, max_value=2**63-1)


@composite
def samples(draw):
    experiment_id = draw(safe_non_empty_strings())

    return Sample(
        experiment_id=experiment_id
    )


@composite
def neighbours(draw):
    experiment_id = draw(safe_non_empty_strings())
    distance = draw(neo4j_integers())

    return Neighbour(
        experiment_id=experiment_id,
        distance=distance
    )


@composite
def nearest_leafs(draw):
    leaf_id = draw(safe_non_empty_strings())
    distance = draw(neo4j_integers())

    return NearestLeaf(
        leaf_id=leaf_id,
        distance=distance
    )
