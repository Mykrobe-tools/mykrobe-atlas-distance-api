from typing import Optional, Union, Any, Callable

from swagger_server.drivers.exceptions import DriverError


class BaseDriver:
    instance: Optional['BaseDriver'] = None

    @classmethod
    def get(cls) -> Union['BaseDriver']:
        if not cls.instance:
            cls.instance = cls.make_instance()
        return cls.instance

    @classmethod
    def make_instance(cls) -> Union['BaseDriver']:
        return cls.attempt(cls._make_instance)

    @classmethod
    def _make_instance(cls) -> Union['BaseDriver']:
        raise NotImplementedError

    def create_new(self, changes: Any):
        self.attempt(self._create_new, changes)

    def _create_new(self, changes: Any):
        raise NotImplementedError

    def apply_changes(self, changes: Any):
        self.attempt(self._apply_changes, changes)

    def _apply_changes(self, changes: Any):
        raise NotImplementedError

    def verify_changes(self, changes: Any) -> bool:
        return self.attempt(self.verify_changes, changes)

    def _verify_changes(self, changes: Any) -> bool:
        raise NotImplementedError

    def execute(self, query: str):
        self.attempt(self._execute, query)

    def _execute(self, query: str):
        raise NotImplementedError

    def clear_db(self):
        self.attempt(self._clear_db)

    def _clear_db(self):
        raise NotImplementedError

    @staticmethod
    def attempt(func: Callable, *args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise DriverError(e) from e
