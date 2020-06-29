from py2neo.ogm import Property

from swagger_server.models import Leaf
from swagger_server.ogm.base import BaseGraphObject


class LeafNode(BaseGraphObject):
    __primarykey__ = 'leaf_id'

    leaf_id = Property()

    model_class = Leaf
