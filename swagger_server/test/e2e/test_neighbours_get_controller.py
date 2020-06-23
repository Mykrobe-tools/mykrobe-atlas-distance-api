from hypothesis import given

from swagger_server.models import Sample, Neighbour
from swagger_server.test.strategies import samples


@given(sample=samples())
def test_getting_neighbours_of_non_existent_sample(sample, get_neighbours):
    assert get_neighbours(sample).status_code == 404


@given(sample=samples())
def test_getting_neighbours_of_existing_sample(sample, create_sample, get_neighbours, sample_graph):
    try:
        if sample.nearest_neighbours:
            for neighbour in sample.nearest_neighbours:
                create_sample(neighbour, ensure=True)

        created = Sample.from_dict(create_sample(sample, ensure=True).json)
        retrieved = [Neighbour.from_dict(x) for x in get_neighbours(sample, ensure=True).json]

        assert len(created.nearest_neighbours) == len(retrieved)
        for neighbour in created.nearest_neighbours:
            assert neighbour in retrieved
    finally:
        sample_graph.delete_all()
