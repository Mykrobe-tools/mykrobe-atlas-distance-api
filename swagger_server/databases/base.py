from abc import ABC, abstractmethod


class BaseDatabase(ABC):

    @abstractmethod
    def apply_schema(self):
        raise NotImplementedError

    @abstractmethod
    def truncate(self):
        raise NotImplementedError
