# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
from api import util


class Submission(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, submitted_at=None, status=None, score=None, commit_hash=None, feedback_available=None):  # noqa: E501
        """Submission - a model defined in OpenAPI

        :param id: The id of this Submission.  # noqa: E501
        :type id: int
        :param submitted_at: The submitted_at of this Submission.  # noqa: E501
        :type submitted_at: datetime
        :param status: The status of this Submission.  # noqa: E501
        :type status: str
        :param score: The score of this Submission.  # noqa: E501
        :type score: float
        :param commit_hash: The commit_hash of this Submission.  # noqa: E501
        :type commit_hash: str
        :param feedback_available: The feedback_available of this Submission.  # noqa: E501
        :type feedback_available: bool
        """
        self.openapi_types = {
            'id': int,
            'submitted_at': datetime,
            'status': str,
            'score': float,
            'commit_hash': str,
            'feedback_available': bool
        }

        self.attribute_map = {
            'id': 'id',
            'submitted_at': 'submitted_at',
            'status': 'status',
            'score': 'score',
            'commit_hash': 'commit_hash',
            'feedback_available': 'feedback_available'
        }

        self._id = id
        self._submitted_at = submitted_at
        self._status = status
        self._score = score
        self._commit_hash = commit_hash
        self._feedback_available = feedback_available

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
    def status(self):
        """Gets the status of this Submission.


        :return: The status of this Submission.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Submission.


        :param status: The status of this Submission.
        :type status: str
        """
        allowed_values = ["submitting", "not_graded", "automatically_graded", "manually_graded"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

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
    def feedback_available(self):
        """Gets the feedback_available of this Submission.


        :return: The feedback_available of this Submission.
        :rtype: bool
        """
        return self._feedback_available

    @feedback_available.setter
    def feedback_available(self, feedback_available):
        """Sets the feedback_available of this Submission.


        :param feedback_available: The feedback_available of this Submission.
        :type feedback_available: bool
        """

        self._feedback_available = feedback_available
