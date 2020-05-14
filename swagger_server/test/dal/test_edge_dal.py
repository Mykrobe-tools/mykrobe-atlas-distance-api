import unittest

from hypothesis import given, assume, strategies as st, settings

from swagger_server.dal.neo4j import Neo4jNode, Neo4jPropertyMapping
from swagger_server.helpers import db
from swagger_server.test.dal import BaseDALTestCase
from swagger_server.test.dal.strategies import NEO4J_EDGE_ST
from swagger_server.test.utils import cleanup_each_example


class TestEdgeDAL(BaseDALTestCase):

    @given(edges=st.lists(NEO4J_EDGE_ST))
    @settings(deadline=None)
    @cleanup_each_example
    def test_connect_to_nodes(self, edges):
        labels = [label for label, _, _ in edges]
        assume(len(labels) == len(set(labels)))
        self.check_empty_db()

        a = Neo4jNode()
        for label, properties, (node_labels, node_props) in edges:
            n = Neo4jNode(node_labels, node_props)
            a.connect(n, label, properties)
        a.create()

        for label, properties, _ in edges:
            properties = Neo4jPropertyMapping(properties)
            rows = db.Neo4jDatabase.get().query(f'MATCH (n)-[:{label} {properties}]->() RETURN n').values()
            self.assertEqual(1, len(rows))

        rows = db.Neo4jDatabase.get().query(f'MATCH (n) RETURN n').values()
        self.assertEqual(len(edges) + 1, len(rows))

    def test_diamond_graph(self):
        """
               node
            /       \
        node        node
            \       /
              node
        """

        self.check_empty_db()

        a, b, c, d = (Neo4jNode(properties={'name': 'n%d' % i}) for i in range(4))
        edge_label = 'EDGE'
        a.connect(b, edge_label)
        a.connect(c, edge_label)
        b.connect(d, edge_label)
        c.connect(d, edge_label)
        a.create()

        rows = db.Neo4jDatabase.get().query(
            f'MATCH '
            f'({{name: "{a.properties["name"]}"}})-[e0:{edge_label}]->({{name: "{b.properties["name"]}"}}),'
            f'({{name: "{a.properties["name"]}"}})-[e1:{edge_label}]->({{name: "{c.properties["name"]}"}}),'
            f'({{name: "{b.properties["name"]}"}})-[e2:{edge_label}]->({{name: "{d.properties["name"]}"}}),'
            f'({{name: "{c.properties["name"]}"}})-[e3:{edge_label}]->({{name: "{d.properties["name"]}"}})'
            f' RETURN e0,e1,e2,e3'
        ).values()
        self.assertEqual(4, len(rows[0]))

        rows = db.Neo4jDatabase.get().query(f'MATCH ()-[e:EDGE]->() RETURN e').values()
        self.assertEqual(4, len(rows))

        rows = db.Neo4jDatabase.get().query(f'MATCH (n) RETURN n').values()
        self.assertEqual(4, len(rows))

    def test_creating_paths(self):
        """
                   node
                /       \
            node         node
           /     \       /    \
        node     node   node   node
        """

        self.check_empty_db()

        a, b, c, d, e, f, g = (Neo4jNode(properties={'name': 'n%d' % i}) for i in range(7))
        edge_label = 'EDGE'
        a.connect(b, edge_label)
        a.connect(c, edge_label)
        b.connect(d, edge_label)
        b.connect(e, edge_label)
        c.connect(f, edge_label)
        c.connect(g, edge_label)
        a.create()

        rows = db.Neo4jDatabase.get().query(
            f'MATCH '
            f'({{name: "{a.properties["name"]}"}})-[e0:{edge_label}]->({{name: "{b.properties["name"]}"}}),'
            f'({{name: "{a.properties["name"]}"}})-[e1:{edge_label}]->({{name: "{c.properties["name"]}"}}),'
            f'({{name: "{b.properties["name"]}"}})-[e2:{edge_label}]->({{name: "{d.properties["name"]}"}}),'
            f'({{name: "{b.properties["name"]}"}})-[e3:{edge_label}]->({{name: "{e.properties["name"]}"}}),'
            f'({{name: "{c.properties["name"]}"}})-[e4:{edge_label}]->({{name: "{f.properties["name"]}"}}),'
            f'({{name: "{c.properties["name"]}"}})-[e5:{edge_label}]->({{name: "{g.properties["name"]}"}})'
            f' RETURN e0,e1,e2,e3,e4,e5'
        ).values()
        self.assertEqual(6, len(rows[0]))

        rows = db.Neo4jDatabase.get().query(f'MATCH ()-[e:EDGE]->() RETURN e').values()
        self.assertEqual(6, len(rows))

        rows = db.Neo4jDatabase.get().query(f'MATCH (n) RETURN n').values()
        self.assertEqual(7, len(rows))


if __name__ == '__main__':
    unittest.main()
