# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from grading_labextension.api.models.base_model_ import Model
from grading_labextension.api import util


class ErrorMessage(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, msg=None):  # noqa: E501
        """ErrorMessage - a model defined in OpenAPI

        :param msg: The msg of this ErrorMessage.  # noqa: E501
        :type msg: str
        """
        self.openapi_types = {
            'msg': str
        }

        self.attribute_map = {
            'msg': 'msg'
        }

        self._msg = msg

    @classmethod
    def from_dict(cls, dikt) -> 'ErrorMessage':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ErrorMessage of this ErrorMessage.  # noqa: E501
        :rtype: ErrorMessage
        """
        return util.deserialize_model(dikt, cls)

    @property
    def msg(self):
        """Gets the msg of this ErrorMessage.


        :return: The msg of this ErrorMessage.
        :rtype: str
        """
        return self._msg

    @msg.setter
    def msg(self, msg):
        """Sets the msg of this ErrorMessage.


        :param msg: The msg of this ErrorMessage.
        :type msg: str
        """

        self._msg = msg
