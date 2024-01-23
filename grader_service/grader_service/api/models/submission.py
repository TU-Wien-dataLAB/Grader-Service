# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from grader_service.api.models.base_model_ import Model
from grader_service.api import util

class Submission(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, submitted_at=None, auto_status=None, manual_status=None, username=None, grading_score=None, score_scaling=None, score=None, assignid=None, commit_hash=None, feedback_status=None, edited=None):  # noqa: E501
        """Submission - a model defined in OpenAPI

        :param id: The id of this Submission.  # noqa: E501
        :type id: int
        :param submitted_at: The submitted_at of this Submission.  # noqa: E501
        :type submitted_at: datetime
        :param auto_status: The auto_status of this Submission.  # noqa: E501
        :type auto_status: str
        :param manual_status: The manual_status of this Submission.  # noqa: E501
        :type manual_status: str
        :param username: The username of this Submission.  # noqa: E501
        :type username: str
        :param grading_score: The grading_score of this Submission.  # noqa: E501
        :type grading_score: float
        :param score_scaling: The score_scaling of this Submission.  # noqa: E501
        :type score_scaling: float
        :param score: The score of this Submission.  # noqa: E501
        :type score: float
        :param assignid: The assignid of this Submission.  # noqa: E501
        :type assignid: int
        :param commit_hash: The commit_hash of this Submission.  # noqa: E501
        :type commit_hash: str
        :param feedback_status: The feedback_status of this Submission.  # noqa: E501
        :type feedback_status: str
        :param edited: The edited of this Submission.  # noqa: E501
        :type edited: bool
        """
        self.openapi_types = {
            'id': int,
            'submitted_at': datetime,
            'auto_status': str,
            'manual_status': str,
            'username': str,
            'grading_score': float,
            'score_scaling': float,
            'score': float,
            'assignid': int,
            'commit_hash': str,
            'feedback_status': str,
            'edited': bool
        }

        self.attribute_map = {
            'id': 'id',
            'submitted_at': 'submitted_at',
            'auto_status': 'auto_status',
            'manual_status': 'manual_status',
            'username': 'username',
            'grading_score': 'grading_score',
            'score_scaling': 'score_scaling',
            'score': 'score',
            'assignid': 'assignid',
            'commit_hash': 'commit_hash',
            'feedback_status': 'feedback_status',
            'edited': 'edited'
        }

        self._id = id
        self._submitted_at = submitted_at
        self._auto_status = auto_status
        self._manual_status = manual_status
        self._username = username
        self._grading_score = grading_score
        self._score_scaling = score_scaling
        self._score = score
        self._assignid = assignid
        self._commit_hash = commit_hash
        self._feedback_status = feedback_status
        self._edited = edited

    @classmethod
    def from_dict(cls, dikt) -> 'Submission':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Submission of this Submission.  # noqa: E501
        :rtype: Submission
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Submission.


        :return: The id of this Submission.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Submission.


        :param id: The id of this Submission.
        :type id: int
        """

        self._id = id

    @property
    def submitted_at(self):
        """Gets the submitted_at of this Submission.


        :return: The submitted_at of this Submission.
        :rtype: datetime
        """
        return self._submitted_at

    @submitted_at.setter
    def submitted_at(self, submitted_at):
        """Sets the submitted_at of this Submission.


        :param submitted_at: The submitted_at of this Submission.
        :type submitted_at: datetime
        """

        self._submitted_at = submitted_at

    @property
    def auto_status(self):
        """Gets the auto_status of this Submission.


        :return: The auto_status of this Submission.
        :rtype: str
        """
        return self._auto_status

    @auto_status.setter
    def auto_status(self, auto_status):
        """Sets the auto_status of this Submission.


        :param auto_status: The auto_status of this Submission.
        :type auto_status: str
        """
        allowed_values = ["not_graded", "pending", "automatically_graded", "grading_failed"]  # noqa: E501
        if auto_status not in allowed_values:
            raise ValueError(
                "Invalid value for `auto_status` ({0}), must be one of {1}"
                .format(auto_status, allowed_values)
            )

        self._auto_status = auto_status

    @property
    def manual_status(self):
        """Gets the manual_status of this Submission.


        :return: The manual_status of this Submission.
        :rtype: str
        """
        return self._manual_status

    @manual_status.setter
    def manual_status(self, manual_status):
        """Sets the manual_status of this Submission.


        :param manual_status: The manual_status of this Submission.
        :type manual_status: str
        """
        allowed_values = ["not_graded", "manually_graded", "being_edited", "grading_failed"]  # noqa: E501
        if manual_status not in allowed_values:
            raise ValueError(
                "Invalid value for `manual_status` ({0}), must be one of {1}"
                .format(manual_status, allowed_values)
            )

        self._manual_status = manual_status

    @property
    def username(self):
        """Gets the username of this Submission.


        :return: The username of this Submission.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this Submission.


        :param username: The username of this Submission.
        :type username: str
        """

        self._username = username

    @property
    def grading_score(self):
        """Gets the grading_score of this Submission.


        :return: The grading_score of this Submission.
        :rtype: float
        """
        return self._grading_score

    @grading_score.setter
    def grading_score(self, grading_score):
        """Sets the grading_score of this Submission.


        :param grading_score: The grading_score of this Submission.
        :type grading_score: float
        """

        self._grading_score = grading_score

    @property
    def score_scaling(self):
        """Gets the score_scaling of this Submission.


        :return: The score_scaling of this Submission.
        :rtype: float
        """
        return self._score_scaling

    @score_scaling.setter
    def score_scaling(self, score_scaling):
        """Sets the score_scaling of this Submission.


        :param score_scaling: The score_scaling of this Submission.
        :type score_scaling: float
        """
        if score_scaling is not None and score_scaling > 1.0:  # noqa: E501
            raise ValueError("Invalid value for `score_scaling`, must be a value less than or equal to `1.0`")  # noqa: E501
        if score_scaling is not None and score_scaling < 0.0:  # noqa: E501
            raise ValueError("Invalid value for `score_scaling`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._score_scaling = score_scaling

    @property
    def score(self):
        """Gets the score of this Submission.


        :return: The score of this Submission.
        :rtype: float
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this Submission.


        :param score: The score of this Submission.
        :type score: float
        """

        self._score = score

    @property
    def assignid(self):
        """Gets the assignid of this Submission.


        :return: The assignid of this Submission.
        :rtype: int
        """
        return self._assignid

    @assignid.setter
    def assignid(self, assignid):
        """Sets the assignid of this Submission.


        :param assignid: The assignid of this Submission.
        :type assignid: int
        """

        self._assignid = assignid

    @property
    def commit_hash(self):
        """Gets the commit_hash of this Submission.


        :return: The commit_hash of this Submission.
        :rtype: str
        """
        return self._commit_hash

    @commit_hash.setter
    def commit_hash(self, commit_hash):
        """Sets the commit_hash of this Submission.


        :param commit_hash: The commit_hash of this Submission.
        :type commit_hash: str
        """

        self._commit_hash = commit_hash

    @property
    def feedback_status(self):
        """Gets the feedback_status of this Submission.


        :return: The feedback_status of this Submission.
        :rtype: str
        """
        return self._feedback_status

    @feedback_status.setter
    def feedback_status(self, feedback_status):
        """Sets the feedback_status of this Submission.


        :param feedback_status: The feedback_status of this Submission.
        :type feedback_status: str
        """

        allowed_values = ["generated", "generating", "not_generated", "generation_failed", "feedback_outdated"]  # noqa: E501
        if feedback_status not in allowed_values:
            raise ValueError(
                "Invalid value for `auto_status` ({0}), must be one of {1}"
                .format(feedback_status, allowed_values)
            )

        self._feedback_status = feedback_status

    @property
    def edited(self):
        """Gets the edited of this Submission.


        :return: The edited of this Submission.
        :rtype: bool
        """
        return self._edited

    @edited.setter
    def edited(self, edited):
        """Sets the edited of this Submission.


        :param edited: The edited of this Submission.
        :type edited: bool
        """

        self._edited = edited
