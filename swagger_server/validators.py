from abc import ABC, abstractmethod
from typing import Tuple


class Validator(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def valid(self) -> Tuple[bool, str]:
        raise NotImplementedError


class SampleValidator(Validator):
    def valid(self) -> Tuple[bool, str]:
        if self.data.nearest_neighbours:
            neighbour_ids = []

            for neighbour in self.data.nearest_neighbours:
                if neighbour.experiment_id in neighbour_ids:
                    return False, 'Ambiguous (duplicated neighbours)'

                neighbour_ids.append(neighbour.experiment_id)

        return True, ''
