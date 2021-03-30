from py2neo import Graph
from py2neo.data import walk
import numpy as np
import json
import argparse
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree


uri = "bolt://localhost:7687"
driver = Graph(uri, auth=("neo4j", "neo3j"))


def get_subgraph_query(uuid):
    return "MATCH(n:SampleNode {experiment_id: \"" + uuid + "\"}) " \
            "CALL apoc.path.subgraphAll(n, {" \
                "relationshipFilter: \"NEIGHBOUR\", " \
                "maxLevel: 1, " \
                "minLevel: 0" \
            "}) " \
            "YIELD nodes, relationships " \
            "RETURN nodes, relationships"


def get_nodes(subgraph):
    return [n['experiment_id'] for n in subgraph[0]['nodes']]


def create_csr_matrix(nodes, relationships):
    num_of_nodes = len(nodes)
    input_matrix = np.zeros((num_of_nodes, num_of_nodes), dtype=np.int8)
    node_index_map = {}
    for index, id in enumerate(nodes):
        node_index_map[id] = index
    for r in relationships:
        start_node, rel, end_node = walk(r)
        start_index = node_index_map[start_node['experiment_id']]
        end_index = node_index_map[end_node['experiment_id']]
        if start_index < end_index:
            input_matrix[start_index][end_index] = rel['distance'] + 1
    return csr_matrix(input_matrix)


def extract_minimum_spanning_tree(nodes, mst):
    relationships = []
    num_of_nodes = len(nodes)
    matrix = mst.toarray()
    for row in range(num_of_nodes - 1):
        for col in range(row + 1, num_of_nodes):
            if matrix[row][col] > 0:
                relationships.append({
                    "start": nodes[row],
                    "end": nodes[col],
                    "distance": int(matrix[row][col] - 1)
                })
    return relationships


parser = argparse.ArgumentParser(description="Generate minimum spanning tree for sample with its nearest neighbours")
parser.add_argument('sample_id', type=str, help='Sample experiment id')
args = parser.parse_args()
query_string = get_subgraph_query(args.sample_id)
subgraph = driver.run(query_string).data()
nodes = get_nodes(subgraph)
input_matrix = create_csr_matrix(nodes, subgraph[0]['relationships'])
mst = minimum_spanning_tree(input_matrix)
print(json.dumps(extract_minimum_spanning_tree(nodes, mst)))
