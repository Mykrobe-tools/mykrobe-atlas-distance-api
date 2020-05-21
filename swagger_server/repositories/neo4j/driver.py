from typing import Union


class Neo4jDriver:
    instance: Union['Neo4jDriver'] = None

    @classmethod
    def get(cls) -> Union['Neo4jDriver']:
        if not cls.instance:
            cls.instance = Neo4jDriver()
        return cls.instance
