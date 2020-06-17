from hypothesis.strategies import composite, text, integers, characters, lists

from swagger_server.models import Sample, Neighbour, NearestLeaf


def safe_non_empty_strings():
    return text(alphabet=characters(whitelist_categories=('L', 'N')), min_size=1)


def int64s():
    return integers(min_value=-2**63, max_value=2**63-1)


@composite
def samples(draw):
    experiment_id = draw(safe_non_empty_strings())
    nearest_neighbours = draw(lists(neighbours()))
    nearest_leaf = draw(nearest_leafs())

    return Sample(
        experiment_id=experiment_id,
        nearest_neighbours=nearest_neighbours,
        nearest_leaf_node=nearest_leaf
    )


@composite
def neighbours(draw):
    experiment_id = draw(safe_non_empty_strings())
    distance = draw(int64s())

    return Neighbour(
        experiment_id=experiment_id,
        distance=distance
    )


@composite
def nearest_leafs(draw):
    leaf_id = draw(safe_non_empty_strings())
    distance = draw(int64s())

    return NearestLeaf(
        leaf_id=leaf_id,
        distance=distance
    )
