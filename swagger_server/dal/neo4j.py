from typing import List, Dict

from swagger_server.helpers import db


class Neo4jDAL:
    @staticmethod
    def create_node(labels: List[str] = None, properties: Dict = None):
        labels = ':' + ':'.join(labels) if labels else ''

        properties = properties if properties else {}
        for k in properties:
            if isinstance(properties[k], str):
                properties[k] = f'"{properties[k]}"'
        properties = [f'{k}:{v}' for k, v in properties.items()]
        properties = '{' + ','.join(properties) + '}'

        q = f'CREATE (n{labels} {properties}) RETURN n'

        return db.Neo4jDatabase.get().query(q).values()[0][0]
