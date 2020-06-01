from hypothesis.strategies import text, composite

from swagger_server.models import Sample


@composite
def samples(draw):
    experiment_id = draw(text())
    return Sample(experiment_id)
