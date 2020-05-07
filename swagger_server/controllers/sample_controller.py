import connexion
from neobolt.exceptions import ConstraintError

from swagger_server.helpers import db
from swagger_server.helpers.controller_helpers import handle_500
from swagger_server.models import Neighbour
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
        if not body.nearest_neighbours:
            query = f'CREATE ({node_variable}:SampleNode {{ name: "{body.experiment_id}" }}) RETURN {node_variable}'
            rows = db.Database.get().query(query).values()
            sample = Sample(rows[0][0]['name'])
        else:
            neighbours = body.nearest_neighbours
            dists = [n.distance for n in neighbours]

            neighbour_variables = [f'n{i}' for i in range(len(neighbours))]
            neighbour_patterns = [f'({v}:SampleNode {{name: "{n.experiment_id}"}})'
                                  for v, n in zip(neighbour_variables, neighbours)]

            rel_variables = [f'r{i}' for i in range(len(dists))]
            rel_patterns = [f'({node_variable})-[{r}:NEIGHBOUR {{dist: {d}}}]->({v})'
                            for r, v, d in zip(rel_variables, neighbour_variables, dists)]

            query = f'CREATE ' \
                    f'({node_variable}:SampleNode {{ name: "{body.experiment_id}" }}),' \
                    f'{",".join(neighbour_patterns)},' \
                    f'{",".join(rel_patterns)} ' \
                    f'RETURN {node_variable},{",".join(neighbour_variables)},{",".join(rel_variables)}'

            rows = db.Database.get().query(query).values()
            neighbour_cols = rows[0][1:1+len(neighbour_variables)]
            rel_cols = rows[0][1+len(neighbour_variables):]
            neighbour_objs = [Neighbour(n['name'], r['dist']) for n, r in zip(neighbour_cols, rel_cols)]
            sample = Sample(rows[0][0]['name'], neighbour_objs)

        return sample, 201
    except ConstraintError as e:
        if 'already exist' not in str(e):
            raise
        return 'Already existed', 409
