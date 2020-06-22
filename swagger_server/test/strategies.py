from hypothesis.strategies import composite, text, integers, characters, lists, one_of, none

from swagger_server.models import Sample, Neighbour, NearestLeaf


def safe_non_empty_strings():
    return text(alphabet=characters(whitelist_categories=('L', 'N')), min_size=1)


def int64s():
    return integers(min_value=-2**63, max_value=2**63-1)


@composite
def samples(draw, has_neighbours=False, unique_neighbours=False, has_leaf=False):
    def neighbours_unique_by(neighbour):
        return neighbour.experiment_id

    neighbours_strategy = lists(
        neighbours(),
        unique_by=neighbours_unique_by if unique_neighbours else None,
        min_size=1 if has_neighbours else 0
    )
    if not has_neighbours:
        neighbours_strategy = one_of(
            neighbours_strategy,
            none()
        )

    nearest_leaf_strategy = nearest_leafs()
    if not has_leaf:
        nearest_leaf_strategy = one_of(
            nearest_leaf_strategy,
            none()
        )

    return Sample(
        experiment_id=draw(safe_non_empty_strings()),
        nearest_neighbours=draw(neighbours_strategy),
        nearest_leaf_node=draw(nearest_leaf_strategy)
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
