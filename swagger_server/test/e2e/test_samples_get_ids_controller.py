from hypothesis import given, strategies as st

from swagger_server.test.strategies import samples, experiment_ids


def test_samples_get_without_any_id(get_sample_by_ids):
    assert get_sample_by_ids('').status_code == 404


@given(sample_ids=st.lists(min_size=1, max_size=5, elements=experiment_ids()))
def test_samples_get_non_existent_ids(sample_ids, get_sample_by_ids):
    assert get_sample_by_ids(",".join(sample_ids)).status_code == 404


@given(samples_with_ids=st.lists(min_size=1, max_size=5,
                                 elements=samples(must_not_have_neighbours=True, must_not_have_leaf=True),
                                 unique_by=lambda x: x.experiment_id))
def test_samples_get_existing_ids(samples_with_ids, create_sample, create_leaf, get_sample_by_ids, sample_graph):
    try:
        created_ids = []
        for sample in samples_with_ids:
            create_sample(sample, ensure=True)
            created_ids.append(sample.experiment_id)

        response = get_sample_by_ids(",".join(created_ids))

        assert response.status_code == 200
        retrieved_ids = [s['experiment_id'] for s in response.json]
        assert len(created_ids) == len(retrieved_ids)
        assert set(created_ids) == set(retrieved_ids)
    finally:
        sample_graph.delete_all()


@given(samples_with_ids=st.lists(min_size=2, max_size=5,
                                 elements=samples(must_not_have_neighbours=True, must_not_have_leaf=True),
                                 unique_by=lambda x: x.experiment_id))
def test_samples_get_partially_existing_ids(samples_with_ids, create_sample, create_leaf, get_sample_by_ids,
                                            sample_graph):
    try:
        generated_ids = []
        created_ids = []
        for index, sample in enumerate(samples_with_ids):
            generated_ids.append(sample.experiment_id)
            if index % 2 == 0:
                continue
            create_sample(sample, ensure=True)
            created_ids.append(sample.experiment_id)

        response = get_sample_by_ids(",".join(generated_ids))

        assert response.status_code == 200
        retrieved_ids = [s['experiment_id'] for s in response.json]
        assert len(created_ids) == len(retrieved_ids)
        assert set(created_ids) == set(retrieved_ids)
        assert len(retrieved_ids) < len(generated_ids)
        assert set(retrieved_ids) < set(generated_ids)
    finally:
        sample_graph.delete_all()
