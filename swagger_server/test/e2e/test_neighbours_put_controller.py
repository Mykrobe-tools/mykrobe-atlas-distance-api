from hypothesis import given
from hypothesis.strategies import lists

from swagger_server.test.strategies import neighbours, experiment_ids


@given(experiment_id=experiment_ids(), new_neighbours=lists(neighbours()))
def test_updating_neighbours_of_non_existent_samples(experiment_id, new_neighbours, update_neighbours, sample_graph):
    assert update_neighbours(experiment_id, new_neighbours).status_code == 404


def test_only_relationships_are_updated():
    pass
