from hypothesis import given

from swagger_server.models import Sample, Neighbour
from swagger_server.test.strategies import samples, experiment_ids


@given(experiment_id=experiment_ids())
def test_getting_neighbours_of_non_existent_sample(experiment_id, get_neighbours):
    assert get_neighbours(experiment_id).status_code == 404


@given(sample=samples())
def test_getting_non_existent_neighbours(sample, create_sample, get_neighbours, sample_graph):
    try:
        create_sample(sample, ensure=True)

        assert get_neighbours(sample.experiment_id).status_code == 404
    finally:
        sample_graph.delete_all()


@given(sample=samples(must_have_neighbours=True))
def test_getting_neighbours_of_existing_sample(sample, create_sample, get_neighbours, sample_graph):
    try:
        for neighbour in sample.nearest_neighbours:
            create_sample(neighbour, ensure=True)

        created = Sample.from_dict(create_sample(sample, ensure=True).json)
        retrieved = [Neighbour.from_dict(x) for x in get_neighbours(sample.experiment_id, ensure=True).json]

        assert len(created.nearest_neighbours) == len(retrieved)
        for neighbour in created.nearest_neighbours:
            assert neighbour in retrieved
    finally:
        sample_graph.delete_all()
