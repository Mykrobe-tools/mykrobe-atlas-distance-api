from typing import Optional

from py2neo import Graph


class Neo4jDriver:
    instance: Optional[Graph] = None
    uri = 'bolt://localhost:7687'
    encrypted = False

    @classmethod
    def get(cls) -> Graph:
        if not cls.instance:
            cls.instance = Graph(cls.uri, secure=cls.encrypted)
        return cls.instance
