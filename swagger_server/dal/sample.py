from neobolt.exceptions import ConstraintError

from swagger_server.helpers import db
from swagger_server.models import Sample, Neighbour, NearestLeaf


class SampleAlreadyExist(Exception):
    pass


class SampleNotExist(Exception):
    pass


def create_sample(sample: Sample) -> Sample:
    try:
        node_variable = 'n'
        neighbour_variables = []
        to_create = [f'({node_variable}:SampleNode {{ name: "{sample.experiment_id}" }})']
        to_return = [node_variable]

        if sample.nearest_neighbours:
            neighbours = sample.nearest_neighbours
            dists = [n.distance for n in neighbours]

            neighbour_variables = [f'n{i}' for i in range(len(neighbours))]
            neighbour_patterns = [f'({v}:SampleNode {{name: "{n.experiment_id}"}})'
                                  for v, n in zip(neighbour_variables, neighbours)]

            rel_variables = [f'r{i}' for i in range(len(dists))]
            rel_patterns = [f'({node_variable})-[{r}:NEIGHBOUR {{dist: {d}}}]->({v})'
                            for r, v, d in zip(rel_variables, neighbour_variables, dists)]

            to_create.append(f'{",".join(neighbour_patterns)}')
            to_create.append(f'{",".join(rel_patterns)}')
            to_return += neighbour_variables + rel_variables

        if sample.nearest_leaf_node:
            leaf_var = 'l'
            lineage_rel_var = 'r'
            to_create.append(f'({leaf_var}:LineageNode {{name: "{sample.nearest_leaf_node.leaf_id}"}})')
            to_create.append(f'({node_variable})-[{lineage_rel_var}:LINEAGE {{dist: {sample.nearest_leaf_node.distance}}}]->({leaf_var})')
            to_return += [leaf_var, lineage_rel_var]

        to_create = ','.join(to_create)
        to_return = ','.join(to_return)
        query = f'CREATE {to_create} RETURN {to_return}'

        rows = db.Neo4jDatabase.get().query(query, write=True).values()
        neighbour_cols = rows[0][1:1+len(neighbour_variables)]
        rel_cols = rows[0][1+len(neighbour_variables):-2]
        neighbour_objs = [Neighbour(n['name'], r['dist']) for n, r in zip(neighbour_cols, rel_cols)]
        leaf = None
        if sample.nearest_leaf_node:
            leaf = NearestLeaf(rows[0][-2]['name'], rows[0][-1]['dist'])
        sample = Sample(rows[0][0]['name'], neighbour_objs, leaf)

        return sample
    except ConstraintError as e:
        if 'already exist' not in str(e):
            raise
        raise SampleAlreadyExist


def get_sample(experiment_id: str) -> Sample:
    rows = db.Neo4jDatabase.get().query(f'MATCH (n:SampleNode {{name: "{experiment_id}"}}) RETURN n').values()

    if not rows:
        raise SampleNotExist

    return Sample(rows[0][0]['name'])


def delete_sample(experiment_id: str):
    rows = db.Neo4jDatabase.get().query(
        f'MATCH (n:SampleNode {{name: "{experiment_id}"}}) DETACH DELETE n RETURN n', write=True).values()

    if not rows:
        raise SampleNotExist


def update_sample(sample: Sample):
    delete_old_neighbours = f'MATCH (n:SampleNode {{name: "{sample.experiment_id}"}}) ' \
                            f'OPTIONAL MATCH (n)-[:NEIGHBOUR]->(ne:SampleNode) ' \
        f'WHERE NOT ne.name IN {[ne.experiment_id for ne in sample.nearest_neighbours]} ' \
        f'DETACH DELETE ne'
    create_new_neighbours = ' '.join([
        f'MERGE (n)-[:NEIGHBOUR {{dist: {n.distance}}}]->(:SampleNode {{name: "{n.experiment_id}"}})'
        for n in sample.nearest_neighbours])

    q = delete_old_neighbours
    if create_new_neighbours:
        q += ' ' + create_new_neighbours
    q += ' RETURN id(n)'

    rows = db.Neo4jDatabase.get().query(q, write=True).values()

    if not rows:
        raise SampleNotExist
