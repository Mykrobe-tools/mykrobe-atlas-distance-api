import pickle
import sys

from py2neo import Graph

from swagger_server.ogm.mappers import SampleNode

if __name__ == '__main__':
    repo = Graph()

    with open(sys.argv[1], 'r') as inf:
        mapping = pickle.load(inf)

    for isolate_id, experiment_id in mapping.items():
        sample = SampleNode.get(isolate_id, repo)
        sample.experiment_id = experiment_id
        repo.push(sample)

