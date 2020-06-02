from abc import ABC, abstractmethod


class BaseDatabase(ABC):
    @abstractmethod
    def truncate(self):
        raise NotImplementedError
