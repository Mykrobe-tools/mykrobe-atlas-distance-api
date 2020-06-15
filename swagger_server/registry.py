from flask import g


def get(name: str):
    if name not in g:
        raise Exception(f'{name} not registered')
    return getattr(g, name)


def register(name: str, obj):
    if name in g:
        raise Exception(f'{name} already registered')
    setattr(g, name, obj)
