# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Distance API",
    author_email="",
    url="",
    keywords=["OpenAPI", "Distance API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    &lt;p&gt;An API for CRUD of two types of distances &lt;li&gt; between a sample and its closest samples &lt;li&gt; between a sample and its closest phylogenetic tree node &lt;p&gt;This API is intended to satisfy the following user stories &lt;li&gt; as a user, I want to add my new sample and its close neighbours so that I can retrieve them later &lt;li&gt; as a user, I want to query a sample for its close neighbours and its nearest node in a phylogenetic tree &lt;li&gt; as a user, I want to query a sample for its close neighbours so that I can do my analysis &lt;li&gt; as a user, I want to query a sample for its nearest node in a phylogenetic tree so that I can do my analysis &lt;li&gt; as a user, I want to update a sample with new list of close neighbours so that they are correct &lt;li&gt; as a user, I want to update a sample with new nearest leaf node in a phylogenetic tree so that it is correct &lt;li&gt; as a user, I want to remove the nearest leaf node in a phylogenetic tree from a sample so that it is correct &lt;li&gt; as a user, I want to remove a sample so that it is no longer available to any users &lt;li&gt; as a user, I want to add a new leaf node to the phylogenetic tree &lt;li&gt; as a user, I want to remove a leaf node from the phylogenetic tree &lt;li&gt; as a user, I want to query a tree node for a list of samples which have this as nearest tree node
    """
)

