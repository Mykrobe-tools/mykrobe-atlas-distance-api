from abc import ABC, abstractmethod


class IDatabase(ABC):
    """ Interface for common methods for databases
    """

    @abstractmethod
    def truncate(self):
        raise NotImplementedError
