from hypothesis import strategies as st

from swagger_server.helpers import db


def capture_logs(func):
    def wrapped(test_case_instance, *args, **kwargs):
        with test_case_instance.assertLogs():
            return func(test_case_instance, *args, **kwargs)

    return wrapped


def cleanup_each_example(func):
    def wrapped(test_case_instance, *args, **kwargs):
        try:
            return func(test_case_instance, *args, **kwargs)
        finally:
            db.Database.get().query('MATCH (n) DETACH DELETE n')

    return wrapped


experiment_id_st = st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1)
