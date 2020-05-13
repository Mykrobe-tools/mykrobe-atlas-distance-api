from typing import List, Dict

from swagger_server.helpers import db


class Neo4jEdge:
    def __init__(self, to, label: str = '', properties: Dict = None):
        self.label = label
        self.properties = properties
        self.to = to

    def build_label(self) -> str:
        return f':{self.label}'

    def build_properties(self) -> str:
        if not self.properties:
            return ''

        properties = self.properties.copy()
        for k, v in properties.items():
            if isinstance(v, str):
                properties[k] = f'"{v}"'
            elif isinstance(v, float):
                properties[k] = '%.7f' % v  # avoid scientific notation
        properties = [f'{k}:{v}' for k, v in properties.items()]

        return '{' + ','.join(properties) + '}'


class Neo4jNode:
    def __init__(self, labels: List[str] = None, properties: Dict = None):
        self.labels = ':' + ':'.join(labels) if labels else ''

        self.properties = properties.copy() if properties else {}
        for k, v in self.properties.items():
            if isinstance(v, str):
                self.properties[k] = f'"{v}"'
            elif isinstance(v, float):
                self.properties[k] = '%.7f' % v  # avoid scientific notation
        self.properties = [f'{k}:{v}' for k, v in self.properties.items()]
        self.properties = '{' + ','.join(self.properties) + '}'

        self.edges = []

    def connect(self, other, label: str = '', properties: Dict = None):
        edge = Neo4jEdge(other, label, properties)
        self.edges.append(edge)

    def create(self):
        self_var = 'n'

        edges = ','.join([f'(n)-[{e.build_label()} {e.build_properties()}]->({e.to.labels} {e.to.properties})' for e in self.edges])

        q = f'CREATE ({self_var}{self.labels} {self.properties})'
        if edges:
            q += f',{edges}'
        q += f' RETURN {self_var}'
        db.Neo4jDatabase.get().query(q, write=True)

    @staticmethod
    def bulk_create(nodes):
        if not nodes:
            return

        variables = ['n%d' % i for i in range(len(nodes))]
        node_part = ','.join([f'({v}{node.labels} {node.properties})' for v, node in zip(variables, nodes)])
        q = f'CREATE {node_part} RETURN {",".join(variables)}'

        db.Neo4jDatabase.get().query(q)
