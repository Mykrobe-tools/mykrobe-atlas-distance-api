import random
from random import randrange, choice

from swagger_server.factories import GraphFactory
from swagger_server.models import Sample, Neighbour, NearestLeaf
from swagger_server.repositories import Neo4jRepository

if __name__ == '__main__':
    repo = Neo4jRepository()

    samples = []

    with open('swagger_server/test/data/sample.list') as f:
        for line in f:
            experiment_id = line.strip()

            sample = Sample(experiment_id)
            sample.nearest_neighbours = []

            node = GraphFactory.build(sample)
            repo.create(node)

            samples.append(sample)

    leaves = [NearestLeaf(str(i)) for i in range(80)]

    for sample in samples:
        n_neighbours = randrange(10, 15)
        sampled = [s for s in random.sample(samples, n_neighbours) if s != sample]

        for s in sampled:
            if sample.experiment_id not in [x.experiment_id for x in s.nearest_neighbours]:
                rel = Neighbour(s.experiment_id, distance=randrange(1, 10))
                sample.nearest_neighbours.append(rel)

        sample.nearest_leaf_node = choice(leaves)

        node = GraphFactory.build(sample)
        repo.update(node)
