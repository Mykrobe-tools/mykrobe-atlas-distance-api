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

    def __getitem__(self, item):
        return self.mapping[item]

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
    def __init__(self, to, label: str, properties: Dict = None):
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
        self.var = ''

    def connect(self, other, label: str, properties: Dict = None):
        edge = Neo4jEdge(other, label, properties)
        self.edges.append(edge)

    def get_all_nodes(self, nodes, node_counter, edges):
        for edge in self.edges:
            if edge.to not in nodes:
                edge.to.var = 'n%d' % node_counter
                nodes.append(edge.to)
                node_counter += 1

            edges.append((self.var, edge, edge.to.var))
            node_counter = edge.to.get_all_nodes(nodes, node_counter, edges)

        return node_counter

    def create(self):
        self.var = 'n'

        nodes = [self]
        edges = []
        self.get_all_nodes(nodes, 0, edges)

        nodes = ','.join([f'({n.var}{n.labels} {n.properties})' for n in nodes])
        edges = ','.join([f'({from_v})-{e.build_query()}->({to_v})' for from_v, e, to_v in edges])

        q = f'CREATE {nodes}'

        if edges:
            q += f',{edges}'

        q += f' RETURN {self.var}'

        db.Neo4jDatabase.get().query(q, write=True)

    @staticmethod
    def bulk_create(nodes):
        if not nodes:
            return

        variables = ['n%d' % i for i in range(len(nodes))]
        node_part = ','.join([f'({v}{node.labels} {node.properties})' for v, node in zip(variables, nodes)])
        q = f'CREATE {node_part} RETURN {",".join(variables)}'

        db.Neo4jDatabase.get().query(q)
