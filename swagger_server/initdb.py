from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from random import sample, randrange

from neomodel import config

from swagger_server.orm.DistanceORM import SampleNode, LineageNode

config.DATABASE_URL = 'bolt://neo4j:@127.0.0.1:7687'
config.ENCRYPTED_CONNECTION = False


N_NODES = 16_000
N_LEAVES = 2000


def get_num_neighbors():
    return randrange(95, 106)


def get_to_know(pair):
    node, neighbors = pair
    with ThreadPoolExecutor() as executor:
        executor.map(lambda s: node.neighbors.connect(s), neighbors)


def connect_with_lineage(pair):
    leaf, samples = pair
    with ThreadPoolExecutor() as executor:
        executor.map(lambda s: s.lineage.connect(leaf), samples)


def main():
    nodes = SampleNode.create(*[{'name': 's%d' % i} for i in range(N_NODES)])
    pairs = []

    for i in range(N_NODES):
        rest = nodes[:i] + nodes[i+1:]
        neighbors = sample(rest, get_num_neighbors())
        node = nodes[i]

        pairs.append((node, neighbors))

    with ProcessPoolExecutor() as executor:
        executor.map(get_to_know, pairs)

    leaves = LineageNode.create(*[{'name': 'l%d' % i} for i in range(N_LEAVES)])
    samples = SampleNode.nodes.all()
    pairs = []

    for leaf in leaves:
        avg_samples_per_leaf = N_NODES / N_LEAVES
        n_to_take_out = randrange(avg_samples_per_leaf - 1, avg_samples_per_leaf + 2)
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
