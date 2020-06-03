from abc import ABC, abstractmethod


class IDatabase(ABC):
    @abstractmethod
    def truncate(self):
        raise NotImplementedError
