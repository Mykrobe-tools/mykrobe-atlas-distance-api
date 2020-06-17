# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class NearestLeaf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, leaf_id=None, distance=None):  # noqa: E501
        """NearestLeaf - a model defined in OpenAPI

        :param leaf_id: The leaf_id of this NearestLeaf.  # noqa: E501
        :type leaf_id: str
        :param distance: The distance of this NearestLeaf.  # noqa: E501
        :type distance: int
        """
        self.openapi_types = {
            'leaf_id': str,
            'distance': int
        }

        self.attribute_map = {
            'leaf_id': 'leaf_id',
            'distance': 'distance'
        }

        self._leaf_id = leaf_id
        self._distance = distance

    @classmethod
    def from_dict(cls, dikt) -> 'NearestLeaf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NearestLeaf of this NearestLeaf.  # noqa: E501
        :rtype: NearestLeaf
        """
        return util.deserialize_model(dikt, cls)

    @property
    def leaf_id(self):
        """Gets the leaf_id of this NearestLeaf.


        :return: The leaf_id of this NearestLeaf.
        :rtype: str
        """
        return self._leaf_id

    @leaf_id.setter
    def leaf_id(self, leaf_id):
        """Sets the leaf_id of this NearestLeaf.


        :param leaf_id: The leaf_id of this NearestLeaf.
        :type leaf_id: str
        """
        if leaf_id is None:
            raise ValueError("Invalid value for `leaf_id`, must not be `None`")  # noqa: E501

        self._leaf_id = leaf_id

    @property
    def distance(self):
        """Gets the distance of this NearestLeaf.


        :return: The distance of this NearestLeaf.
        :rtype: int
        """
        return self._distance

    @distance.setter
    def distance(self, distance):
        """Sets the distance of this NearestLeaf.


        :param distance: The distance of this NearestLeaf.
        :type distance: int
        """
        if distance is None:
            raise ValueError("Invalid value for `distance`, must not be `None`")  # noqa: E501

        self._distance = distance
