# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from grader_labextension.api.models.base_model_ import Model
from grader_labextension.api.models.submission_period import SubmissionPeriod
from grader_labextension.api import util

from grader_labextension.api.models.submission_period import SubmissionPeriod  # noqa: E501

class AssignmentSettings(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, late_submission=None):  # noqa: E501
        """AssignmentSettings - a model defined in OpenAPI

        :param late_submission: The late_submission of this AssignmentSettings.  # noqa: E501
        :type late_submission: List[SubmissionPeriod]
        """
        self.openapi_types = {
            'late_submission': List[SubmissionPeriod]
        }

        self.attribute_map = {
            'late_submission': 'late_submission'
        }

        self._late_submission = late_submission

    @classmethod
    def from_dict(cls, dikt) -> 'AssignmentSettings':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The AssignmentSettings of this AssignmentSettings.  # noqa: E501
        :rtype: AssignmentSettings
        """
        return util.deserialize_model(dikt, cls)

    @property
    def late_submission(self):
        """Gets the late_submission of this AssignmentSettings.


        :return: The late_submission of this AssignmentSettings.
        :rtype: List[SubmissionPeriod]
        """
        return self._late_submission

    @late_submission.setter
    def late_submission(self, late_submission):
        """Sets the late_submission of this AssignmentSettings.


        :param late_submission: The late_submission of this AssignmentSettings.
        :type late_submission: List[SubmissionPeriod]
        """

        self._late_submission = late_submission