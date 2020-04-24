from concurrent.futures.process import ProcessPoolExecutor
from random import sample, random, randrange

from neomodel import db, config

from swagger_server.orm.DistanceORM import SampleNode

config.DATABASE_URL = 'bolt://neo4j:@127.0.0.1:7687'
config.ENCRYPTED_CONNECTION = False


N_NODES = 16_000


def get_num_neighbors():
    return randrange(95, 106)


def get_to_know(pair):
    node, neighbors = pair
    for n2 in neighbors:
        query = f'MATCH (n1:SampleNode),(n2:SampleNode) WHERE n1.name="{node.name}" AND n2.name="{n2.name}" ' \
                f'CREATE (n1)-[:NEIGHBOR {{dist: {random()}}}]->(n2) ' \
                f'RETURN n1,n2 '
        db.cypher_query(query)


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


if __name__ == '__main__':
    main()
