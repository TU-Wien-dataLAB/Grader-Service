# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from grading_labextension.api.models.base_model_ import Model
from grading_labextension.api import util


class Assignment(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, type=None, due_date=None, status=None, points=None):  # noqa: E501
        """Assignment - a model defined in OpenAPI

        :param id: The id of this Assignment.  # noqa: E501
        :type id: int
        :param name: The name of this Assignment.  # noqa: E501
        :type name: str
        :param type: The type of this Assignment.  # noqa: E501
        :type type: str
        :param due_date: The due_date of this Assignment.  # noqa: E501
        :type due_date: datetime
        :param status: The status of this Assignment.  # noqa: E501
        :type status: str
        :param points: The points of this Assignment.  # noqa: E501
        :type points: float
        """
        self.openapi_types = {
            'id': int,
            'name': str,
            'type': str,
            'due_date': datetime,
            'status': str,
            'points': float
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'type': 'type',
            'due_date': 'due_date',
            'status': 'status',
            'points': 'points'
        }

        self._id = id
        self._name = name
        self._type = type
        self._due_date = due_date
        self._status = status
        self._points = points

    @classmethod
    def from_dict(cls, dikt) -> 'Assignment':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Assignment of this Assignment.  # noqa: E501
        :rtype: Assignment
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Assignment.


        :return: The id of this Assignment.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Assignment.


        :param id: The id of this Assignment.
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Assignment.


        :return: The name of this Assignment.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Assignment.


        :param name: The name of this Assignment.
        :type name: str
        """

        self._name = name

    @property
    def type(self):
        """Gets the type of this Assignment.


        :return: The type of this Assignment.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Assignment.


        :param type: The type of this Assignment.
        :type type: str
        """
        allowed_values = ["user", "group"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def due_date(self):
        """Gets the due_date of this Assignment.


        :return: The due_date of this Assignment.
        :rtype: datetime
        """
        return self._due_date

    @due_date.setter
    def due_date(self, due_date):
        """Sets the due_date of this Assignment.


        :param due_date: The due_date of this Assignment.
        :type due_date: datetime
        """

        self._due_date = due_date

    @property
    def status(self):
        """Gets the status of this Assignment.


        :return: The status of this Assignment.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Assignment.


        :param status: The status of this Assignment.
        :type status: str
        """
        allowed_values = ["created", "pushed", "released", "fetching", "fetched", "complete"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def points(self):
        """Gets the points of this Assignment.


        :return: The points of this Assignment.
        :rtype: float
        """
        return self._points

    @points.setter
    def points(self, points):
        """Sets the points of this Assignment.


        :param points: The points of this Assignment.
        :type points: float
        """

        self._points = points
