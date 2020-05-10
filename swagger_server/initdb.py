from random import sample, randrange

from swagger_server.helpers import db

db.URI = "bolt://localhost:7687"
db.ENCRYPTED = False


N_LEAVES = 2043


def get_num_samples_per_leaf():
    return randrange(5)


def get_num_neighbors():
    return randrange(5, 16)


def get_to_know(pair):
    node, neighbors = pair
    neighbour_names = [n['name'] for n in neighbors]

    query = f'MATCH (a),(b) WHERE a.name=\'{node["name"]}\' AND b.name in {neighbour_names} ' \
            f'CREATE (a)-[:NEIGHBOUR {{ dist: {randrange(20)} }}]->(b)'
    db.Neo4jDatabase.get().query(query)


def connect_with_lineage(pair):
    leaf, samples = pair
    sample_names = [n['name'] for n in samples]

    query = f'MATCH (a),(b) WHERE a.name=\'{leaf["name"]}\' AND b.name in {sample_names} ' \
            f'CREATE (b)-[:LINEAGE {{ dist: {randrange(10)} }}]->(a)'
    db.Neo4jDatabase.get().query(query)


def create_nodes(names):
    variables = [f'n{i}' for i in range(len(names))]
    props = [f'{{name:"{name}"}}' for name in names]
    nodes = [f'({v}:SampleNode {p})' for v, p in zip(variables, props)]

    query = 'CREATE ' + ','.join(nodes) + ' RETURN ' + ','.join(variables)
    return db.Neo4jDatabase.get().query(query).values()[0]


def create_leaves():
    variables = [f'n{i}' for i in range(N_LEAVES)]
    props = [f'{{ name: "leaf_{str(i).zfill(len(str(N_LEAVES)))}" }}' for i in range(N_LEAVES)]
    nodes = [f'({v}:LineageNode {p})' for v, p in zip(variables, props)]

    query = 'CREATE ' + ','.join(nodes) + ' RETURN ' + ','.join(variables)
    return db.Neo4jDatabase.get().query(query).values()[0]


def main():
    with open('swagger_server/test/data/sample.list') as sample_list:
        nodes = create_nodes([name.rstrip() for name in sample_list])
    pairs = []

    for i in range(len(nodes)):
        rest = nodes[:i] + nodes[i+1:]
        neighbors = sample(rest, get_num_neighbors())
        node = nodes[i]

        pairs.append((node, neighbors))

    for p in pairs:
        get_to_know(p)

    leaves = create_leaves()
    pairs = []

    for leaf in leaves:
        if not nodes:
            break

        n_to_take_out = get_num_samples_per_leaf()
        n_to_take_out = min(n_to_take_out, len(nodes))

        took_out = []
        for _ in range(n_to_take_out):
            took_out.append(nodes.pop(randrange(len(nodes))))

        pairs.append((leaf, took_out))

    # Leftover samples
    if nodes:
        pairs[-1] = (pairs[-1][0], pairs[-1][1] + nodes)

    for p in pairs:
        connect_with_lineage(p)


if __name__ == '__main__':
    main()
