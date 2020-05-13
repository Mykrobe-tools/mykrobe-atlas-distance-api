from typing import List, Dict

from swagger_server.helpers import db


class Neo4jProperty:
    def __init__(self, v):
        if isinstance(v, str):
            self.value = f'"{v}"'
        elif isinstance(v, float):
            self.value = '%.7f' % v  # avoid scientific notation
        else:
            self.value = v


class Neo4jPropertyMapping:
    def __init__(self, properties: Dict):
        self.mapping = properties.copy() if properties else None

    def __str__(self):
        if not self.mapping:
            return ''

        m = {}

        for k, v in self.mapping.items():
            m[k] = Neo4jProperty(v).value
        m = [f'{k}:{v}' for k, v in m.items()]

        return '{' + ','.join(m) + '}'


class Neo4jLabelList:
    def __init__(self, labels: List[str]):
        self.labels = labels

    def __str__(self):
        return ':' + ':'.join(self.labels) if self.labels else ''


class Neo4jEdge:
    def __init__(self, to, label: str = '', properties: Dict = None):
        self.label = label
        self.properties = Neo4jPropertyMapping(properties)
        self.to = to

    def build_query(self) -> str:
        return f'[:{self.label} {self.properties}]'


class Neo4jNode:
    def __init__(self, labels: List[str] = None, properties: Dict = None):
        self.labels = Neo4jLabelList(labels)
        self.properties = Neo4jPropertyMapping(properties)
        self.edges = []

    def connect(self, other, label: str = '', properties: Dict = None):
        edge = Neo4jEdge(other, label, properties)
        self.edges.append(edge)

    def get_all_nodes(self, nodes):
        for edge in self.edges:
            if edge.to not in nodes:
                nodes.append(edge.to)
                edge.to.get_all_nodes(nodes)

    def create(self):
        self_var = 'n'

        nodes = []
        self.get_all_nodes(nodes)
        variables = ['n%d' % i for i in range(len(nodes))]

        edges = ','.join([f'(n)-{e.build_query()}->({v})' for v, e in zip(variables, self.edges)])

        q = f'CREATE ({self_var}{self.labels} {self.properties})'

        for v, node in zip(variables, nodes):
            q += f',({v}{node.labels} {node.properties})'

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
