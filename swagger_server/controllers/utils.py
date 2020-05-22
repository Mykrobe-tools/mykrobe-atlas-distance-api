from flask import current_app

from swagger_server.models import Error


def handle_unexpected_errors(func):
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            current_app.logger.error(e)
            return Error(500, "Unexpected error"), 500

    return wrapped
