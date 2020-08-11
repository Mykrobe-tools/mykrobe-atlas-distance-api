from hypothesis.strategies import composite, text, integers, characters, lists, one_of, none

from swagger_server.models import Sample, Neighbour, NearestLeaf, Leaf


def experiment_ids():
    return text(alphabet=characters(whitelist_categories=('L', 'N')), min_size=1)


def leaf_ids():
    return text(alphabet=characters(whitelist_categories=('L', 'N')), min_size=1)


def distances():
    return integers(min_value=-2 ** 63, max_value=2 ** 63 - 1)


@composite
def samples(draw, must_have_neighbours=False, must_have_leaf=False, leaf_id=None, must_not_have_neighbours=False,
            must_not_have_leaf=False):
    experiment_id = draw(experiment_ids())

    neighbours_strategy = lists(
        neighbours().filter(lambda x: x.experiment_id != experiment_id),
        unique_by=lambda x: x.experiment_id,
        min_size=1 if must_have_neighbours else 0
    )
    if not must_have_neighbours:
        neighbours_strategy = one_of(
            neighbours_strategy,
            none()
        )
    if must_not_have_neighbours:
        neighbours_strategy = none()

    nearest_leaf_strategy = nearest_leaves(leaf_id)
    if not must_have_leaf:
        nearest_leaf_strategy = one_of(
            nearest_leaf_strategy,
            none()
        )
    if must_not_have_leaf:
        nearest_leaf_strategy = none()

    return Sample(
        experiment_id=experiment_id,
        nearest_neighbours=draw(neighbours_strategy),
        nearest_leaf_node=draw(nearest_leaf_strategy)
    )


@composite
def neighbours(draw):
    experiment_id = draw(experiment_ids())
    distance = draw(distances())

    return Neighbour(
        experiment_id=experiment_id,
        distance=distance
    )


@composite
def nearest_leaves(draw, leaf_id=None):
    leaf_id = leaf_id or draw(experiment_ids())
    distance = draw(distances())

    return NearestLeaf(
        leaf_id=leaf_id,
        distance=distance
    )


@composite
def leaves(draw):
    leaf_id = draw(leaf_ids())

    return Leaf(
        leaf_id=leaf_id
    )


@composite
def trees(draw):
    leaf = draw(leaves())
    sample_list = draw(lists(samples(must_have_leaf=True, leaf_id=leaf.leaf_id), unique_by=lambda x: x.experiment_id))

    return leaf, sample_list
