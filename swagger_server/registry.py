"""
The `registry` module provides an interface to register and retrieve shared objects in the entire application.
"""

from typing import Any

from flask import g


def get(name: str) -> Any:
    if name not in g:
        raise Exception(f'{name} not registered')
    return getattr(g, name)


def register(name: str, obj):
    if name in g:
        raise Exception(f'{name} already registered')
    setattr(g, name, obj)
