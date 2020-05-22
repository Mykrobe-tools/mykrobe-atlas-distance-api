from swagger_server.ogm import SampleNode
from swagger_server.models import Sample


class SampleRepository:
    @staticmethod
    def create(sample: Sample) -> SampleNode:
        node = SampleNode()
        node.name = sample.experiment_id

        return node
