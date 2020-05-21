from typing import Union

from neo4j import GraphDatabase


class Neo4jDriver:
    instance: Union['Neo4jDriver'] = None
    uri = 'bolt://localhost:7687'
    encrypted = False

    def __enter__(self):
        self.driver = GraphDatabase.driver(self.uri, encrypted=self.encrypted)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    @classmethod
    def get(cls) -> Union['Neo4jDriver']:
        if not cls.instance:
            cls.instance = Neo4jDriver()
        return cls.instance
