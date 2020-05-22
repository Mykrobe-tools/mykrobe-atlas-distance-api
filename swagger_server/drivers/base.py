from typing import Optional, Union, Any


class BaseDriver:
    instance: Optional['BaseDriver'] = None

    @classmethod
    def get(cls) -> Union['BaseDriver']:
        if not cls.instance:
            cls.instance = cls.make_instance()
        return cls.instance

    @classmethod
    def make_instance(cls) -> Union['BaseDriver']:
        raise NotImplementedError

    def create_new(self, changes: Any):
        raise NotImplementedError

    def apply_changes(self, changes: Any):
        raise NotImplementedError

    def verify_changes(self, changes: Any) -> bool:
        raise NotImplementedError

    def execute(self, query: str):
        raise NotImplementedError

    def clear_db(self):
        raise NotImplementedError
