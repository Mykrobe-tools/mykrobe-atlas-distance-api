import connexion
from neobolt.exceptions import ConstraintError

from swagger_server.helpers import db
from swagger_server.helpers.controller_helpers import handle_500
from swagger_server.models import Neighbour, NearestLeaf, Error
from swagger_server.models.sample import Sample  # noqa: E501


@handle_500
def samples_post(body):  # noqa: E501
    """samples_post

    Add a new sample. Duplicates are not allowed # noqa: E501

    :param body: Sample to be added
    :type body: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        body = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    try:
        node_variable = 'n'
        neighbour_variables = []
        to_create = [f'({node_variable}:SampleNode {{ name: "{body.experiment_id}" }})']
        to_return = [node_variable]

        if body.nearest_neighbours:
            neighbours = body.nearest_neighbours
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

        if body.nearest_leaf_node:
            leaf_var = 'l'
            lineage_rel_var = 'r'
            to_create.append(f'({leaf_var}:LineageNode {{name: "{body.nearest_leaf_node.leaf_id}"}})')
            to_create.append(f'({node_variable})-[{lineage_rel_var}:LINEAGE {{dist: {body.nearest_leaf_node.distance}}}]->({leaf_var})')
            to_return += [leaf_var, lineage_rel_var]

        to_create = ','.join(to_create)
        to_return = ','.join(to_return)
        query = f'CREATE {to_create} RETURN {to_return}'

        rows = db.Neo4jDatabase.get().query(query).values()
        neighbour_cols = rows[0][1:1+len(neighbour_variables)]
        rel_cols = rows[0][1+len(neighbour_variables):-2]
        neighbour_objs = [Neighbour(n['name'], r['dist']) for n, r in zip(neighbour_cols, rel_cols)]
        leaf = None
        if body.nearest_leaf_node:
            leaf = NearestLeaf(rows[0][-2]['name'], rows[0][-1]['dist'])
        sample = Sample(rows[0][0]['name'], neighbour_objs, leaf)

        return sample, 201
    except ConstraintError as e:
        if 'already exist' not in str(e):
            raise
        return Error(409, 'Already existed'), 409
