from typing import List, Dict

from swagger_server.helpers import db


class Neo4jNode:
    labels = ''
    properties = ''

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

        self.labels = labels
        self.properties = properties

    def create(self):
        q = f'CREATE (n{self.labels} {self.properties}) RETURN n'
        db.Neo4jDatabase.get().query(q)

    @staticmethod
    def bulk_create(nodes):
        if not nodes:
            return

        variables = ['n%d' % i for i in range(len(nodes))]
        node_part = ','.join([f'({v}{node.labels} {node.properties})' for v, node in zip(variables, nodes)])
        q = f'CREATE {node_part} RETURN {",".join(variables)}'

        db.Neo4jDatabase.get().query(q)
