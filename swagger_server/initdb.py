from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from random import sample, randrange

from neomodel import config

from swagger_server.orm.DistanceORM import SampleNode, LineageNode

config.DATABASE_URL = 'bolt://neo4j:@127.0.0.1:7687'
config.ENCRYPTED_CONNECTION = False


N_LEAVES = 2043


def get_num_samples_per_leaf():
    return randrange(5)


def get_num_neighbors():
    return randrange(5, 16)


def get_to_know(pair):
    node, neighbors = pair
    with ThreadPoolExecutor() as executor:
        executor.map(lambda s: node.neighbors.connect(s, {'dist': randrange(20)}), neighbors)


def connect_with_lineage(pair):
    leaf, samples = pair
    with ThreadPoolExecutor() as executor:
        executor.map(lambda s: s.lineage.connect(leaf, {'dist': randrange(10)}), samples)


def main():
    with open('swagger_server/test/data/sample.list') as sample_list:
        nodes = SampleNode.create(*[{'name': name.rstrip()} for name in sample_list])
    pairs = []

    for i in range(len(nodes)):
        rest = nodes[:i] + nodes[i+1:]
        neighbors = sample(rest, get_num_neighbors())
        node = nodes[i]

        pairs.append((node, neighbors))

    with ProcessPoolExecutor() as executor:
        executor.map(get_to_know, pairs)

    leaves = LineageNode.create(*[{'name': f'leaf_{i}'.zfill(len(str(N_LEAVES)))} for i in range(N_LEAVES)])
    samples = SampleNode.nodes.all()
    pairs = []

    for leaf in leaves:
        if not samples:
            break

        n_to_take_out = get_num_samples_per_leaf()
        n_to_take_out = min(n_to_take_out, len(samples))

        took_out = []
        for _ in range(n_to_take_out):
            took_out.append(samples.pop(randrange(len(samples))))

        pairs.append((leaf, took_out))

    # Leftover samples
    if samples:
        pairs[-1] = (pairs[-1][0], pairs[-1][1] + samples)

    with ProcessPoolExecutor() as executor:
        executor.map(connect_with_lineage, pairs)


if __name__ == '__main__':
    main()
