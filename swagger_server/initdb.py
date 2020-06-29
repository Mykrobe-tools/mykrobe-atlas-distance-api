import random
from random import randrange, choice

from py2neo import Graph

from swagger_server.models import Sample, Neighbour, NearestLeaf
from swagger_server.ogm.sample_node import SampleNode

if __name__ == '__main__':
    repo = Graph()

    samples = []

    with open('swagger_server/test/data/sample.list') as f:
        for line in f:
            experiment_id = line.strip()

            sample = Sample(experiment_id)
            sample.nearest_neighbours = []

            SampleNode.create(sample, repo)

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

        SampleNode.update(sample.experiment_id, repo, neighbours=sample.nearest_neighbours, leaf=sample.nearest_leaf_node)
