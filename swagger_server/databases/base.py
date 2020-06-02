from abc import ABC, abstractmethod
from typing import Any


class BaseDatabase(ABC):

    @abstractmethod
    def create(self, obj: Any):
        raise NotImplementedError

    @abstractmethod
    def truncate(self):
        raise NotImplementedError
