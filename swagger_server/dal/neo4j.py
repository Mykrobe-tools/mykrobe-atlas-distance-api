from typing import List, Dict

from swagger_server.helpers import db


class Neo4jNode:
    def __init__(self, labels: List[str] = None, properties: Dict = None):
        labels = ':' + ':'.join(labels) if labels else ''

        properties = properties.copy() if properties else {}
        for k, v in properties.items():
            if isinstance(v, str):
                properties[k] = f'"{v}"'
            elif isinstance(v, float):
                properties[k] = '%.7f' % v  # avoid scientific notation
        properties = [f'{k}:{v}' for k, v in properties.items()]
        properties = '{' + ','.join(properties) + '}'

        q = f'CREATE (n{labels} {properties}) RETURN n'

        db.Neo4jDatabase.get().query(q)
