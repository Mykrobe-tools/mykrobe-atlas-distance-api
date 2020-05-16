from flask import current_app

from swagger_server.helpers import db


def get_nearest_neighbours(sample_id):
    result = db.Neo4jDatabase.get().query(
        f'MATCH (:SampleNode {{name: "{sample_id}"}})-[r:NEIGHBOUR]-(m:SampleNode) RETURN '
        f'r.dist,m.name'
    ).values()

    return [{'experiment_id': r[1], 'distance': r[0]} for r in result]


def get_nearest_leaf_node(sample_id):
    result = db.Neo4jDatabase.get().query(
        f'MATCH (:SampleNode {{name: "{sample_id}"}})-[r:LINEAGE]->(m:LineageNode) RETURN '
        f'r.dist,m.name').values()

    if not result:
        if current_app.config['DEBUG']:
            current_app.logger.debug({
                'error': 'sample or lineage not exist',  # we don't know which one here so we log it out for debug later
                'sample_id': sample_id
            })

        return {}

    if len(result) > 1:
        current_app.logger.error({
            'error': 'sample has more than 1 lineage',
            'sample_id': sample_id
        })

    return {'leaf_id': result[0][1], 'distance': result[0][0]}
